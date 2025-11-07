from micropyGPS import MycropyGPS
from machine import UART, Pin
import time

gps = MicropyGPS()
uart = UART(2, baudrate=9600, tx=17, rx=16)

def procesar_gps():
    while True:
        if uart.any():
            datos = uart.read()
            for byte in datos:
                gps.update(chr(byte))  # Procesa cada carácter
            print(f"Latitud: {gps.latitude}, Longitud: {gps.longitude}")
        time.sleep(1)

procesar_gps()