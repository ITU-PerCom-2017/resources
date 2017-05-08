import binascii
import pycom
import socket
import time
from network import LoRa
from machine import I2C
from struct import unpack

# Colors
off = 0x000000
red = 0xff0000
green = 0x00ff00
blue = 0x0000ff

# Turn off heartbeat LED
pycom.heartbeat(False)

# Initialize LoRaWAN radio
lora = LoRa(mode=LoRa.LORAWAN)

# Set network keys
app_eui = binascii.unhexlify('70B3D57EF0003F19')
app_key = binascii.unhexlify('17162A7852BEFCB8C742C52671E45359')

# Join the network
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
pycom.rgbled(red)

# Loop until joined
while not lora.has_joined():
    print('Not joined yet...')
    pycom.rgbled(off)
    time.sleep(0.1)
    pycom.rgbled(red)
    time.sleep(2)

print('Joined')
pycom.rgbled(blue)

# Set up socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
s.setblocking(True)

def evaluate(a):
    v = unpack('<H', a)[0]
    return (v >> 8) + ((v & 0xFF) << 8)  # Divide by 10 to get Celsius value (e.g. from int 269 to 26,9 C)

def preparePacket(dataId,  value):
    res = bytes ( [ dataId, (value & 0xFF00) >> 8, (value & 0x00FF) ] )
    print (dataId,  value)
    return res

sensorId = 0x20 # == 32

# Registers
moistureRegister = 0
temperatureRegister = 5
lightRegister = 4

#Receiver IDs
tempId = 0xAA
moistId = 0xBB
lightId = 0xCC

# Sensor readings
i2c = I2C(0, I2C.MASTER, baudrate=10000)

while True:
    # Continuously read data
    i2c.writeto(sensorId, '\x03') # Light is special
    time.sleep(1.5)
    aLight = i2c.readfrom_mem(sensorId, lightRegister, 2)
    aTemp = i2c.readfrom_mem(sensorId, temperatureRegister, 2)
    aMoist = i2c.readfrom_mem(sensorId, moistureRegister, 2)
    
    # Prepare byte arrays for all the sensor data
    temp = preparePacket(tempId,  evaluate(aTemp))
    moist = preparePacket(moistId,  evaluate(aMoist))
    light = preparePacket(lightId,  evaluate(aLight))
    
    # Send the three values to the beacon
    countTemp = s.send(temp)
    countMoist = s.send(moist)
    countLight = s.send(light)
    
    # Wait an amount of time (sampling frequency)
    print('Sleeping')
    pycom.rgbled(green)
    time.sleep(10)
    print('Woke up')
    pycom.rgbled(blue)
