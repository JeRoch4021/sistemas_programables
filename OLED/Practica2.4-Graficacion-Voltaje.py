'''
Integrantes del equipo:
Rocha Sainez Jeshua Isaac
Becerra Quezada Fabricio

Objetivo del programa:
Conectar un potenciómetro al pin analógico del ESP32 y mostrar en
la pantalla OLED una gráfica en tiempo real del voltaje leído, en
esta visualización se debe proyectar una representación gráfica
(gráfico de barras o lineal) que se actualice dinámicamente
'''

import machine
import ssd1306
from time import sleep

i2c = machine.SoftI2C(scl=machine.Pin(15), sda=machine.Pin(4))

pin = machine.Pin(16, machine.Pin.OUT)
pin.value(0) #Configura GPIO16 en bajo para resetear el OLED
pin.value(1) #Mientras que el OLED esté ejecutándose, GPIO16 debe estar en 1

oled_ancho = 128
oled_alto = 64
oled = ssd1306.SSD1306_I2C(oled_ancho, oled_alto, i2c)
oled.fill_rect(5, 3, 14, 12, 1) # Dibuja un rectángulo relleno iluminado. Origen (5, 3)y anchura x altura 14x12 píxels

oled.show() # Muestra el resultado
sleep(2) # Espera 2 segundos
oled.fill(1) # Rellena la pantalla (la ilumina entera)
oled.fill_rect(5, 3, 14, 12 ,0) # Dibuja un rectángulo relleno apagado. Origen (5, 3)y anchura x altura 14x12 píxels

oled.show() # Muestra el resultado