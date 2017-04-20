from machine import UART
import os
import network
uart = UART(0, 115200)
os.dupterm(uart)

wlan = network.WLAN()
wlan.deinit()
