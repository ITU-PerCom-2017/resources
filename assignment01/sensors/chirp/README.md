# Chirp: Plant Watering Sensor

https://wemakethings.net/chirp/

This module has three different sensors: temperature, light and soil moisture.a
Chirp acts is a I2C slave, you can get its values from the LoPy (I2C master).
Read more about I2C [here](https://learn.sparkfun.com/tutorials/i2c).
Every group should have one of these.


## Temperature

- thermistor for measurement
- 10th of degrees in Celsius (e.g., 260 is 26 C)


## Light

- uses a LED for measurement
- values range from 0 to 65535
- Note: 0 is maximal light and 65535 is total darkness

## Moisture

- uses [capacitive sensing](https://en.wikipedia.org/wiki/Capacitive_sensing),
  more on this technique
  [here](https://wemakethings.net/2012/09/26/capacitance_measurement/)
- 290-310 in free air, 251 in medium dry soil, 672 in water 
