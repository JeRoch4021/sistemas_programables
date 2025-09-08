'''
Integrantes del equipo:
Rocha Sainez Jeshua Isaac
Becerra Quezada Fabricio

Objetivo del programa:
Ingresar dentro de la matriz 9x9 los números enteros N necesarios para dibujar un icono
en la pantalla OLED, los cuales serán recibidos como parámetros por la función escalar
creada para modificar el tamaño original del icono
'''

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

# La funcion cambiarTamanioIcono recibe los parametros: 
# icono (espera una matriz de lista de listas con los 0 y 1 que representan el icono)
# oled (el objeto de pantalla que tiene el metodo, pixel(x,y,color) y show())
# x0, y0 (coordenadas de inicio que indica donde dibujar el icono)
# escala (la ampliación)
def cambiarTamanioIcono(icono, oled, x0=0, y0=0, escala=1):
    # Recorre las filas de la matriz, donde 
    # y: es el índice de fila, 
    # fila: es la lista con los valores de esa fila
    for y, fila in enumerate(icono): # Dibuja los puntos de la matriz
        # Recorre la columna de cada variable fila (la lista de valores), donde
        # x: es el índice de la columna,
        # c: es el valor del elemento
        for x, c in enumerate(fila):
            if c: # Si c es igual a 1
                # Este for repite el pixel original por cada fila 
                # (de manera vertical hacia abajo) según la escala
                for dy in range(escala):
                    # Este for repite el pixel original por cada columna
                    # (de manera horizontal hacia la derecha) según la escala
                    for dx in range(escala):
                        # Llamada al objeto de pantalla 
                        oled.pixel(x0 + x*escala + dx, y0 + y*escala + dy, c)
    oled.show()

cambiarTamanioIcono(ICONO, oled, 10, 10, 4)
