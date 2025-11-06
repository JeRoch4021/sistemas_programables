from machine import UART
import time

gps = UART(2, baudrate=9600, tx=13, rx=15)

while True:
    if gps.any():
        print(gps.readline())
    time.sleep(1)
