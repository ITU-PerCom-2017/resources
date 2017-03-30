# Chirp: Plant Watering Sensor

Check out the manufacturer documentation: https://wemakethings.net/chirp/
Details, pcb, sensors: https://github.com/Miceuz/i2c-moisture-sensor

This module has three different sensors: temperature, light and soil moisture.a
Chirp acts is a I2C slave, you can get its values from the LoPy (I2C master).
Read more about I2C [here](https://learn.sparkfun.com/tutorials/i2c).
Every group should have one of these.


## Temperature

- thermistor for measurement
- 10th of degrees in Celsius (e.g., 260 is 26 C)

Here s the thermistor, 
marked "TH1" on the pcb:
http://www.murata.com/en-eu/products/productdetail?partno=NCP18XH103F03RB


## Light

- uses a LED for measurement, marked "D3" on the pcb.
http://uk.farnell.com/kingbright/kp-1608surck/led-0603-230mcd-red/dp/2290329

- values range from 0 to 65535
- Note: 0 is maximal light and 65535 is total darkness

## Moisture

- uses [capacitive sensing](https://en.wikipedia.org/wiki/Capacitive_sensing),
  more on this technique
  [here](https://wemakethings.net/2012/09/26/capacitance_measurement/)
- 290-310 in free air, 251 in medium dry soil, 672 in water 

## I2C and Byte Unpacking

**Note: The repl-console is a great tool to interactively try out your code.**

After you have connected the sensor like shown on the pictures,
you can scan for devices on the I2C bus to get the sensor's ID:

```Python
from machine import I2C
i2c = I2C(0, I2C.MASTER, baudrate=10000)
i2c.scan()
```

This should return you the default address of the chirp sensor: `0x20` (`32`).

Knowing the address, you can get the actual sensor data.
Capacitive register (moisture): `0`

Temperature register: `5`

Light register: `4`



```Python
from machine import I2C
i2c = I2C(0, I2C.MASTER, baudrate=10000)
register = 5  # for temperature
a = i2c.readfrom_mem(0x20, register, 2)
```

Note: For the light sensor you need to first request to "take a measurement", sleep and then the value!

```Python
i2c.writeto(0x20, '\x03')
...
```

`a` is a bytearray. You need to unpack it to get a number.
In python you can use the struct module for that:


```Python
from struct import unpack
a = bytearray(b'\x01\r')
v = unpack('<H', a)[0]  # Should return 3329
```

Now that we have a number, we can convert it to the actual value, in this case
the temperature:

```Python
v = 3329
temperature = (v >> 8) + ((v & 0xFF) << 8)  # Should return 269
```
