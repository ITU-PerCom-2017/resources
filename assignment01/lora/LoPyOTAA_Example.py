import binascii
import pycom
import socket
import time
from network import LoRa

__author__ = "Sebastian Buettrich"

# Colors
off = 0x000000
red = 0xff0000
green = 0x00ff00
blue = 0x0000ff

# Turn off hearbeat LED
pycom.heartbeat(False)

# Initialize LoRaWAN radio
lora = LoRa(mode=LoRa.LORAWAN)

# Set network keys
app_eui = binascii.unhexlify('YOUR_APPEUI')
app_key = binascii.unhexlify('YOUR_APPKEY')

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

s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
s.setblocking(True)

i = 0
while True:
    count = s.send(bytes([i % 256]))
    print('Sent %s bytes' % count)
    pycom.rgbled(green)
    time.sleep(0.1)
    pycom.rgbled(blue)
    time.sleep(9.9)
    i += 1
