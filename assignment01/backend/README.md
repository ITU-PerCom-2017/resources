# Backend

We use the things network (TTN) to help us with coordinating IDs and keys of your
LoPys.

TTN has the notion of an application. Each application has a unique APPEUI.
We use one application for all our LoPys:
"dk-cph-itu-pitlab-01". An application has devices associated to it. A single
LoPy represents a device and has a unique device ID in TTN.
You can browse this information for our application on [TTN's
console](https://console.thethingsnetwork.org/).

For more details on TTN see thethingsnetwork [wiki](https://www.thethingsnetwork.org/wiki).


## MQTT

TTN runs a MQTT broker. MQTT is a pub/sub protocol by IBM and is widely used in
IoT applications. You can follow [this
tutorial](http://www.hivemq.com/blog/mqtt-essentials-part-1-introducing-mqtt)
or read more on it on its [wikipedia page](https://en.wikipedia.org/wiki/MQTT).

TTN has a quickstart page on how to get started with MQTT and how to subscribe to
messages of an application.
Try to follow [the steps](https://www.thethingsnetwork.org/docs/applications/mqtt/quick-start.html).

Note: our application ID is: dk-cph-itu-pitlab-01
You can find your Access Key when you scroll down on TTN: "ttn-account-v2...."


## Our Backend

We use BTrDB, a database developed by a group at UC Berkeley, to store time
series data. You can find a paper on BTrDB
[here](https://www.usenix.org/conference/fast16/technical-sessions/presentation/andersen).

We have some small middleware running that subscribes to the message stream of
our application (i.e., all packets sent by all LoPys). Our middleware then
creates a unique ID and adds the time series data into our BTrDB instance.
MongoDB is used to store metadata for a time series (e.g., what kind of sensor,
what unit, what location etc...).

There is a [plotter](http://130.226.142.195) which allows to browse this added
sensor data in time (look under "Instrumentation_Test").


## Protocol

We send bytes from LoPy to gateway.
TTN has a [short
introduction](https://www.thethingsnetwork.org/docs/devices/bytes.html) on
bytes, hex numbers, byte arrays and encoding.

In brief, with a byte we can represent 0-255. Because we have values greater
than 255 (e.g., for the light and moisture sensor) and we do not want to loose
the decimal place for temperature values, we need to use >1byte.
E.g., using two bytes we can already encode 65536 values.

For sending a value > 255, we thus use one byte to represent the left byte
and one to represent the right byte.

E.g., for sending a light value this would be:

```python
light = 15356
light_id = 0xCC
bytes = bytearray(3)
bytes[0] = light_id
bytes[1] = (light & 0xFF00) >> 8
bytes[2] = (light & 0x00FF)
```

We use one byte to identify the sensor type:

- Chirp/Temperature   0xAA
- Chirp/Moisture      0xBB
- Chirp/Light         0xCC

To add sensor data from a sensor to the backend, you need to follow that protocol.
Please send an email or make a pull request to add another type of sensor (then
we can create another identifier).
