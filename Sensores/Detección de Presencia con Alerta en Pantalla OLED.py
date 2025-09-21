"""
Integrantes:
    Rocha Sainez Jeshua Isaaac
    Becerra Quezada Fabricio
    
Objetivo:
    Desarrollar un programa en Python que implemente un sistema de monitoreo continuo utilizando un sensor ultrasónico y
    un sensor PIR (infrarrojo pasivo). El sistema deberá mostrar en una pantalla OLED la distancia a objetos en tiempo real y,
    ante la detección de una fuente de calor (presencia humana o animal), activar una rutina de alerta visual dinámica mediante
    interrupciones. Esta rutina deberá ir más allá de un simple mensaje, incorporando efectos visuales como iconos, animaciones,
    parpadeo de pantalla o imágenes.
"""

from hcsr04 import HCSR04 
from machine import Pin, ADC, SoftI2C
import ssd1306
import time
import framebuf
from images import (LOGO)

# Configuración de la pantalla OLED 
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Configuración del sensor ultrasónico
sensor = HCSR04(trigger_pin=15, echo_pin=12, echo_timeout_us=10000)

# PIR con interrupción
PIR_Interrupt = Pin(13, Pin.IN)

# Adjuntar interrupción externa a GPIO13 y flanco 
# Ascendente como fuente de evento externo  

# Variable global
Motion_Detected = False

def handle_interrupt(Pin):
    global Motion_Detected
    Motion_Detected = True
    
PIR_Interrupt.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)

def iniciar():
    # Mostrar en la OLED los datos del equipo y el logo del Tecnológico
    oled.fill(0)
    buffer = bytearray(LOGO)
    logo_tec = framebuf.FrameBuffer(buffer, 128, 64, framebuf.MONO_HLSB) # Convierte el formato de LOGO en binario

    # Mostrar logo del ITL
    oled.blit(logo_tec, 0, 0)
    oled.show()
    sleep_ms(3000)
    
    # Mostrar el nombre de los integrantes
    oled.fill(0)
    oled.text('Sistemas programables', 0, 0)
    oled.text('Jeshua Rocha', 0, 10)
    oled.text('Fabricio Becerra', 0, 20)
    oled.show()
    sleep_ms(3000)
    
    # Mostrar el objetivo de la practica
    oled.fill(0)
    oled.text('Objetivo:', 0, 0)
    oled.text('Monitoreo con', 0, 15)
    oled.text('ultrasonico + PIR', 0, 30)
    oled.show()
    sleep_ms(3000)
    
def alerta_presencia():
    # Rutina de alerta de 5s con parpadeo y animación simple
    star = time.ticks_ms()
    
    while time.ticks_diff(time.ticks_ms(), start) < 5000:
        oled.fill(0)
        oled.text("¡¡¡AlERTA!!!", 10, 10)
        oled.text("Deteccion de", 10, 30)
        oled.text("PRESENCIA", 20, 45)
        led.show()
        time.sleep(0.5)
        
        # Simulamos un parpadeo apagando la pantalla
        oled.fill(0)
        oled.show()
        tiem.sleep(0.5)

def mostrar_distancia():
    """Leer el ultrasónico y muestra distancia con validación"""
    try:
        distancia = sensor.distance_cm()
        
        # Validación de errores comunes en HCSR04
        if distancia in (250, -1, 0):
            oled.fill(0)
            oled.text("ERROR:", 0, 0)
            oled.text("Lectura no válida", 0, 15)
            oled.show()
            print("ERROR: Lectura no válida")
        else:
            estado = "Objeto detectado" if distancia < 100 else "No hay objeto"
            oled.fill(0)
            oled.text(estado, 0, 0)
            oled.text("Dist: {} cm".format(int(distancia)), 0, 20)
            oled.text("Estado: OK", 0, 40)
            oled.show()
            print("Distancia:", distancia, "cm")
    except Exception as ex:
        oled.fill(0)
        oled.text("ERROR sensor", 0, 0)
        oled.show()
        print("Excepcion en:", ex)
        
    
if __name__ == '__main__':
    iniciar()
    
    while True:
        if Motion_Detected:
            alerta_presencia()
            Motion_Detected = False # Reiniciar bandera
        else:
            mostrar_distancia()
            time.sleep(1)
