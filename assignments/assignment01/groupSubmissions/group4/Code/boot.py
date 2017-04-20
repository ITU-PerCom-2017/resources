from machine import UART
from network import WLAN
import os

uart = UART(0, 115200)
os.dupterm(uart)
wlan = WLAN()
wlan.deinit()
