import machine
import ssd1306
from time import sleep
i2c = machine.SoftI2C(scl=machine.Pin(22), sda=machine.Pin(21))
pin = machine.Pin(16, machine.Pin.OUT)
pin.value(0) 
#Configura  GPIO16 en bajo para resetear el OLED
pin.value(1) 
#Mientras que el  OLED esté ejecutándose, GPIO16 debe estar en 1
oled_ancho = 128
oled_alto = 64
oled = ssd1306.SSD1306_I2C(oled_ancho, oled_alto, i2c)

ICONO = [ # Matriz de puntos
    [ 0, 0, 0, 1, 1, 1, 0, 0, 0],
    [ 0, 1, 1, 1, 1, 1, 1, 1, 0],
    [ 0, 1, 0, 0, 1, 0, 0, 1, 0],
    [ 1, 1, 0, 0, 1, 0, 0, 1, 1],
    [ 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [ 1, 1, 0, 0, 0, 0, 0, 1, 1],
    [ 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [ 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [ 1, 0, 1, 0, 1, 0, 1, 0, 1],
]

for y, fila in enumerate(ICONO): # Dibuja los puntos de la matriz 
    for x, c in enumerate(fila):
        oled.pixel(x, y, c)

oled.show()
