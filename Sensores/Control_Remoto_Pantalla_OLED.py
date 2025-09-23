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
import ssd1306, framebuf, time
from time import sleep_ms
from images import (LOGO)
from ir_rx import NEC_16

# Configuración del OLED
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Configuración IR
ir_pin = Pin(15, Pin.IN) # Receptor IR en GPIO15

# Diccionario de códigos del control
codigos = {
    "1": 0x45,
    "2": 0x46,
    "3": 0x47,
    "4": 0x44,
    "5": 0x40,
    "6": 0x43,
    "7": 0x7,
    "8": 0x15,
    "9": 0x9,
    "*": 0x16,
    "0": 0x19,
    "#": 0xd,
    "UP": 0x18,
    "DOWN": 0x52,
    "LEFT": 0x8,
    "RIGHT": 0x5a,
    "OK": 0x1c
    }

# Variable globales
opcion_menu = 1
total_opciones = 3
# Etiqueta para identificar el estado del menu por el IR
estado_menu = "MENU"

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

posiciones_y_menu = {
    1: 20,
    2: 35,
    3: 50
}

# FUNCIONES DE PANTALLLA
# Menu sin flecha
def mostrar_menu():
    oled.fill(0)
    oled.text("MENU PRINCIPAL", 0, 9)
    # Opción 1
    oled.text("1. Deteccion", 12, 20)
    # Opción 2
    oled.text("2. Icono", 12, 35)
    # Opción 3
    oled.text("3. Logo/Datos", 12, 50)
    oled.show()
    
# Animación de la flecha
def animar_flecha(opcion_anterior, opcion_actual):
    y_inicial = posiciones_y_menu[opcion_anterior]
    y_final = posiciones_y_menu[opcion_actual]
    
    # Direccion del movimiento
    paso = 1 if y_final > y_inicial else -1
    
    # Mover flecha pixel por piexel
    for y in range(y_inicial, y_final + paso, paso):
        mostrar_menu()
        oled.text(">", 0, y)
        oled.show()
        sleep_ms(10) # Ajustar velocidad
    

def deteccion_botones_ctrl_remoto(codigo):
    oled.fill(0)
    oled.text("Opcion 1:", 0, 0)
    oled.text("Botones IR", 0, 12)
    oled.text("Codigo:", 0, 28)
    oled.text(str(hex(codigo)), 0, 40) # Mostrar código hexadecimal
    oled.show()
    
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
    
def control_icono():
    oled.fill(0)
    oled.text("Opcion 2:", 0, 0)
    oled.text("Tam.Icono: " + str(tam_icono), 0, 12)
    escala = max(1, tam_icono//5)
    # Dibujamos el icono que en anteriores practicas hicimos
    cambiarTamanioIcono(ICONO, oled, 40, 30, escala)
    oled.show()
        
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
    oled.text('Ctrl.Remoto+OLED', 0, 10)
    oled.text('Fecha: 25/09/2025', 0, 20)
    oled.show()
    sleep_ms(3000)
    
# CALLBACK IR
def callback_ir(data, addr, ctrl):
    """
    NEC_16 devuelve data de 16 bits
    """
    
    global estado_menu, opcion_menu, tam_icono
    print("Boton IR recibido:", hex(data)) # Debug de consola
    
    if estado_menu == "MENU":
        # Navegación con flechas
        if data == codigos["UP"]:
            opcion_anterior = opcion_menu
            opcion_menu -= 1
            if opcion_menu < 1:
                opcion_menu = total_opciones
            animar_flecha(opcion_anterior, opcion_menu)
            
        elif data == codigos["DOWN"]:
            opcion_anterior = opcion_menu
            opcion_menu += 1
            if opcion_menu > total_opciones:
                opcion_menu = 1
            animar_flecha(opcion_anterior, opcion_menu)
            
        # Navegación del menu principal 
        elif data == codigos["OK"]:
            if opcion_menu == 1: estado_menu = "OP1"
            elif opcion_menu == 2: estado_menu = "OP2"
            elif opcion_menu == 3: estado_menu = "OP3"
            
    if estado_menu == "OP1":
        deteccion_botones_ctrl_remoto(data)
        if data in [codigos["*"], codigos["#"]]: # Al presinar esto botones se regresara al menu principal
            estado_menu = "MENU"
    
    # Control icono
    if estado_menu == "OP2":
        if data == codigos["UP"]:
            tam_icono = min(tam_icono + 1, tam_max)
        elif data == codigos["DOWN"]:
            tam_icono = max(tam_icono - 1, tam_min)
        elif data in [codigos["*"], codigos["#"]]: # Al presinar esto botones se regresara al menu principal
            estado_menu = "MENU"
        control_icono()
            
    if estado_menu == "OP3":
        mostrar_logo_datos()
        estado_menu = "MENU"

# Iniciar receptor IR
ir = NEC_16(ir_pin, callback_ir)

# Bucle principal
if __name__ == '__main__':
    while True:
        if estado_menu == "MENU":
            mostrar_menu()
        time.sleep(20)
    
    
    
    
    

