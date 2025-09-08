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
pin_04.measure()

# Método para inniciar la presentacion del programa
def iniciar():
    # Mostrar en la OLED los datos del equipo y el logo del Tecnológico
    return

def mostrarLuminosidad():
    return

def mostrarTemperatura():
    return

def mostrarHumedad():
    return

def mostrarIntegrantes():
    return

# Ejecución de las opciones del menú
def menu(opcion):
    case 1:
        return mostrarLuminosidad()
    case 2:
        return mostrarTemperatura()
    case 3:
        return mostrarHumedad()
    case 4:
        return mostrarIntegrantes()
    
if __name__ == '__main__':
    iniciar()
    while True:
        optn = int(input("Ingresa la opción que desees visualizar"))
        if optn <5 and optn > 0:
            menu(optn)
        else:
            print("ERROR. Opción incorrecta")
