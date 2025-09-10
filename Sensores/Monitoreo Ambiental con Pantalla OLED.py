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

# Ejecución de las opciones del menú
def menu(opcion):
    case 1:
        return mostrarLuminosidad()
    case 2:
        return mostrarTemperatura()
    case 3:
        return mostrarHumedad()
    
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
