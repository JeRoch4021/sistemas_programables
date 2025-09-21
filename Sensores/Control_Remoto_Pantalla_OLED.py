"""
Integrantes:
    Rocha Sainez Jeshua Isaaac
    Becerra Quezada Fabricio
    
Objetivo:
    Desarrollar un único programa en Python que integre tres funcionalidades distintas, las cuales
    serán seleccionadas y ejecutadas mediante un menú controlado por un control remoto infrarrojo
    (IR). El sistema mostrará la información en una pantalla OLED y permitirá al usuario navegar
    entre las opciones de forma interactiva.
"""

from machine import Pin, ADC, SoftI2C
import ssd1306
import time
import framebuf
from images import (LOGO)
from ir_rx import NEC_16

# Configuración del OLED
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Configuración IR
ir_pin = Pin(15, Pin.IN) # Receptor IR en GPIO15

# Diccionario de códigos del control
codigos = {
    "1": 0x00FFA25D,
    "2": 0x00FF629D,
    "3": 0x00FFE21D,
    "4": 0x00FF22DD,
    "5": 0x00FF02FD,
    "6": 0x00FFC23D,
    "7": 0x00FFE01F,
    "8": 0x00FFA857,
    "9": 0x00FF906F,
    "*": 0x00FF6897,
    "0": 0x00FF9867,
    "#": 0x00FFB04F,
    "UP": 0x00FF18E7,
    "DOWN": 0x00FF4AB5,
    "LEFT": 0x00FF10EF,
    "RIGHT": 0x00FF5AA5,
    "OK": 0x00FF38C7
    }

# Variable globales
opcion_menu = 1
total_opciones = 3

tam_icono = 10
tam_min = 5
tam_max = 30


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

# Nos traemos el método para escalar el icono de la anterior practica
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

# FUNCIONES DE PANTALLLA
def mostrar_menu():
    oled.fill(0)
    oled.text("--MENU PRINCIPAL--", 0, 9)
    
    # Opción 1
    prefix = "> " if opcion_menu == 1 else "  "
    oled.text(prefix + "1. Deteccion", 0, 15)
    
    # Opción 2
    prefix = "> " if opcion_menu == 2 else "  "
    oled.text(prefix + "2. Icono", 0, 30)
    
    # Opción 3
    prefix = "> " if opcion_menu == 3 else "  "
    oled.text(prefix + "3. Logo/Datos", 0, 45)
    
    oled.show()

def deteccion_botones_ctrl_remoto(codigo):
    oled.fill(0)
    oled.text("Opcion 1:", 0, 0)
    oled.text("Botones IR", 0, 12)
    oled.text("Codigo:", 0, 28)
    oled.text(str(codigo), 0, 40)
    oled.show()
    
def control_icono():
    oled.fill(0)
    oled.text("Opcion 2:", 0, 0)
    oled.text("Tam.Icono: " + str(tam_icono), 0, 12)
    # Dibujamos el icono que en anteriores practicas hicimos
    cambiarTamanioIcono(ICONO, oled, 40, 20, tam_icono//5)
        
def mostrar_logo_datos():
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
    oled.text('Integrantes:', 0, 0)
    oled.text('Sis.Programables', 0, 10)
    oled.text('Jeshua Rocha', 0, 20)
    oled.text('Fabricio Becerra', 0, 30)
    oled.show()
    sleep_ms(3000)
    
    # Mostrar el nombre de la practica y la fecha
    oled.fill(0)
    oled.text('Practica:', 0, 0)
    oled.text('Ctrl.Remoto + OLED', 0, 10)
    oled.text('Fecha: 25/09/2025', 0, 20)
    oled.show()
    sleep_ms(3000)
    
# CALLBACK IR
ultimo_codigo = None
    
def callback_ir(data, addr, ctrl):
    """
    NEC_16 devuelve data de 16 bits
    """
    
    global ultimo_codigo, opcion_menu, tam_icono
    
    ultimo_codigo = data
    print("Boton IR recibido:", hex(data)) # Debug de consola
    
    # Navegación con flechas
    if data == codigos["UP"]:
        opcion_menu -= 1
        if opcion_menu < 1:
            opcion_menu = total_opciones
    elif data == codigos["DOWN"]:
        opcion_menu += 1
        if opcion_menu > total_opciones:
            opcion_menu = 1
            
    elif data == codigo["OK"]:
        if opcion_menu == 1:
            deteccion_botones_ctrl_remoto(ultimo_codigo)
        elif opcion_menu == 2:
            control_icono()
        elif opcion_menu == 3:
            mostrar_logo_datos()
        
    # Control icono
    if opcion_menu == 2:
        if data == codigos["RIGHT"]:
            tam_icono += 1
            if tam_icono > tam_max:
                tam_icono = tam_max
            control_icono()
        elif data == codigos["LEFT"]:
            tam_icono -= 1
            if tam_icono < tam_min:
                tam_icono = tam_min
            control_icono()

if __name__ == '__main__':
    while True:
        mostrar_menu()
        time.sleep(0.2)
    
    
    
    
    

