"""
Integrantes:
    Rocha Sainez Jeshua Isaaac
    Becerra Quezada Fabricio
    
Objetivo:
    Desarrollar un programa en Python que permita medir y visualizar en tiempo real los niveles de luminosidad, temperatura y humedad
    de un ambiente, utilizando sensores y una pantalla OLED. El sistema debe presentar un menú interactivo que permita al usuario
    seleccionar qué parámetro visualizar, mostrando una gráfica en tiempo real durante 20 segundos. Al finalizar el tiempo, el menú
    debe regresar automáticamente.
"""
from machine import Pin, ADC, SoftI2C
from dht import DHT11
import ssd1306
import time
from utime import sleep_ms
from images import (LOGO)

#Configuración de la pantalla OLED 
i2c = SoftI2C(scl=machine.Pin(22), sda=machine.Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
#Configuración de la fotorresistencia
ldr = ADC(Pin(34))
ldr.atten(ADC.ATTN_11DB)
#Configuración de DHT11
pin_04 = DHT11(Pin(4)) # crea el objeto pin_04 para un módulo DHT11 en el pin 04

# Método para inniciar la presentacion del programa
def iniciar():
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
    # Mostrar el menu
    desplegarMenu()

# Método para  mostrar en pantalla los valores de luminosidad durante 20 seg en la pantalla 
def mostrarLuminosidad():
    valor = ldr.read()
    oled.text(str(valor), 0, 0)
    return

# Método para  mostrar en pantalla los valores de temperatura durante 20 seg en la pantalla 
def mostrarTemperatura():
    pin_04.measure()
    temperatura = pin_04.temperature()
    return

# Método para  mostrar en pantalla los valores de humedad durante 20 seg en la pantalla 
def mostrarHumedad():
    pin_04.measure
    humedad = pin_04.humidity()
    return

def desplegarMenu():
    olde.fill(0)
    oled.text('Presione: ')
    oled.text('1. Luminosidad', 0, 10)
    oled.text('2. Temperatura', 0, 20)
    oled.text('3. Humedad', 0, 30)

def grafica(parametro):
    oled.fill(0)
    oled.text("Graficando:", 0, 0)
    oled.text(parametro, 0, 10)
    oled.show()
    sleep_ms(1000)

    start_time = time.ticks_ms()
    x = 0  # posición en X

    # Dibujar ejes básicos
    oled.fill(0)
    oled.line(0, 63, 127, 63, 1)   # eje X
    oled.line(0, 20, 0, 63, 1)     # eje Y
    oled.show()

    while time.ticks_diff(time.ticks_ms(), start_time) < 20000:  # 20 segundos
        # --- Lectura según parámetro ---
        if parametro == "luminosidad":
            valor = ldr.read()              # 0 - 4095
            valor = int((valor/4095)*43)    # escalar a 0-43 (área gráfica)

        elif parametro == "temperatura":
            pin_04.measure()
            valor = pin_04.temperature()    # ej. 0-50 °C
            valor = int((valor/50)*43)

        elif parametro == "humedad":
            pin_04.measure()
            valor = pin_04.humidity()       # ej. 0-100 %
            valor = int((valor/100)*43)

        # --- Graficar ---
        y = 63 - valor   # invertir para que valores altos suban
        if x < 128:
            oled.pixel(x, y, 1)
        else:
            # Si se llena la pantalla, reinicia
            oled.fill(0)
            oled.line(0, 63, 127, 63, 1)
            oled.line(0, 20, 0, 63, 1)
            x = 0

        oled.show()
        sleep_ms(500)  # muestra cada 0.5s
        x += 2         # avanza 2 px por lectura

    # --- Termina el tiempo: regresar al menú ---
    oled.fill(0)
    desplegarMenu()
    oled.show()
    

# Ejecución de las opciones del menú
def menu(opcion):
    if opcion == 1:
        grafica("luminosidad")
    elif opcion == 2:
        grafica("temperatura")
    elif opcion == 3:
        grafica("humedad")
    
if __name__ == '__main__':
    iniciar()
    while True:
        optn = int(input("Ingresa la opción que desees visualizar"))
        if optn < 4 and optn > 0:
            menu(optn)
            time_ms(20000)
            desplegarMenu()
        else:
            print("ERROR. Opción incorrecta")
            oled.text("ERROR.", 0,0)
            oled.text('Opción incorrecta', 0, 10)
            desplegarMenu()
