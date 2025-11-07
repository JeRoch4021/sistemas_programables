# Implementación de librerias
from micropyGPS import MicropyGPS
from machine import UART, Pin
import time

# Parámetros de configuración GPS
gps = MicropyGPS()
uart = UART(2, baudrate=9600, tx=13, rx=15, timeout=10)

def procesar_gps():
    while True:
        # Leer todos los bytes disponibles del buffer UART
        if uart.any():
            # Leer bloque de datos (bytes)
            datos = uart.read()
            if datos:
                # Procesar cada byte por byte con MicropyGPS
                for byte in datos:
                    gps.update(chr(byte))  # Procesa cada carácter
            # Impresión para verificar que los valores sean correctos
            print("\n*** GPS Status ***")
            print(f"Fix status: {'Valid' if gps.valid else 'Searching...'}")
            print(f"Latitud: {gps.latitude_string()}, Longitud: {gps.longitude_string()}")
            print(f"Altitud: {gps.altitude} m")
            print(f"Velocidad: {gps.speed_string('kph')} ({gps.compass_direction()})")
            print(f"Tiempo UTC: {gps.timestamp[0]:02}:{gps.timestamp[1]:02}:{int(gps.timestamp[2]):02}s")
            print(f"Fecha: {gps.date}")
        # Instrucción de retardo para no saturar la CPU
        time.sleep(0.5)

# Llamada al método para probar el código
procesar_gps()