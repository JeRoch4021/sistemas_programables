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

#Configuración de la pantalla OLED 
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

#Configuración del sensor ultrasónico
sensor = HCSR04(trigger_pin=15, echo_pin=12, echo_timeout_us=10000)

#PIR
PIR_Interrupt = Pin(13, Pin.IN)

#Adjuntar interrupción externa a GPIO13 y flanco 
#ascendente como fuente de evento externo
PIR_Interrupt.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)  

#Variable global
Motion_Detected = False

def handle_interrupt(Pin):
    global Motion_Detected
    Motion_Detected = True

def iniciar():
    oled.fill(0)
    # Mostrar en la OLED los datos del equipo y el logo del Tecnológico
    buffer = bytearray(LOGO)
    logo_tec = framebuf.FrameBuffer(buffer, 128, 64, framebuf.MONO_HLSB) # Convierte el formato de LOGO en binario

    oled.fill(0)
    # mostrar logo del ITL
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
    
if __name__ == '__main__':
    iniciar()
    while True:
        if Motion_Detected:
            oled.fill(0)
            oled.text("¡Detección de presencia!", 0, 0)
            oled.show()
            time.sleep(5)
        else:
            distance= sensor.distance_cm()
            text = 'Distancia:', str(distance), 'cm'
            print(text)
            oled.fill(0)
            oled.text(text, 0, 0)
            oled.show()
            time.sleep(5)
