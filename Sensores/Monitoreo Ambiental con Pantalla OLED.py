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
import framebuf
from images import (LOGO)

#Configuración de la pantalla OLED 
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
#Configuración de la fotorresistencia
ldr = Pin(25, Pin.IN)
#Configuración de DHT11
pin_04 = DHT11(Pin(4)) # crea el objeto pin_04 para un módulo DHT11 en el pin 04

# Método para iniciar la presentacion del programa
def iniciar():
    # Mostrar en la OLED los datos del equipo y el logo del Tecnológico
    buffer = bytearray(LOGO)
    logo_tec = framebuf.FrameBuffer(buffer, 128, 64, framebuf.MONO_HLSB) # Convierte el formato de LOGO en binario
    oled.fill(0)
    
    # mostrar logo del ITL
    oled.blit(logo_tec, 30, 0)
    oled.show()
    sleep_ms(3000)
    # Mostrar el nombre de los integrantes
    oled.fill(0)
    oled.text('Sis.Programables', 0, 0)
    oled.text('Integrantes:', 0, 10)
    oled.text('Jeshua Rocha', 0, 20)
    oled.text('Fabricio Becerra', 0, 30)
    oled.show()
    sleep_ms(3000)
    oled.fill(0)
    # Mostrar el menu
    desplegarMenu()

# Método para  mostrar en pantalla los valores de luminosidad durante 20 seg en la pantalla 
def mostrarLuminosidad():
    luminosidad = ldr.value()
    return luminosidad

# Método para mostrar en pantalla los valores de temperatura durante 20 seg en la pantalla 
def mostrarTemperatura():
    temperatura = pin_04.temperature()
    return temperatura

# Método para mostrar en pantalla los valores de humedad durante 20 seg en la pantalla 
def mostrarHumedad():
    humedad = pin_04.humidity()
    return humedad

# Metodo para mostrar el menu
def desplegarMenu():
    oled.fill(0)
    oled.text('Presione: ', 0, 0)
    oled.text('1. Luminosidad', 0, 10)
    oled.text('2. Temperatura', 0, 20)
    oled.text('3. Humedad', 0, 30)
    oled.show()
    
def leerLuminosidadBinaria():
    # Devuelve el porcentaje aproximado de luminosidad usando el pin DO
    conteo = 0
    muestras = 10
    for _ in range(muestras):
        conteo += 1 - mostrarLuminosidad() # Ahora es solo 0 o 1
        sleep_ms(20) # Leer cada 20s
    porcentaje = int ((conteo/muestras)*100)
    return porcentaje

def dibujarEjes(parametro):
    oled.fill(0)
    # Ejes
    oled.line(35, 63, 127, 63, 1) # Eje x
    oled.line(35, 20, 35, 63, 1) #Eje Y
    
    # Etiquetas Y según el parámetro recibido
    if parametro == "luminosidad":
        oled.text("100%", 0, 20)
        oled.text("50%", 0, 40)
        oled.text("0%", 0, 56)
    elif parametro == "temperatura":
        oled.text("50C", 0, 20)
        oled.text("25C", 0, 40)
        oled.text("0C", 0, 56)
    elif parametro == "humedad":
        oled.text("100%", 0, 20)
        oled.text("50%", 0, 40)
        oled.text("0%", 0, 56)
    
    # Etiquetas X (tiempo)
    oled.text("0", 32, 0)
    oled.text("5", 47, 0)
    oled.text("10", 63, 0)
    oled.text("15", 86, 0)
    oled.text("20", 112, 0)
    
    oled.show()
    
def grafica(parametro):
    oled.fill(0)
    oled.text("Graficando:", 0, 0)
    oled.text(parametro, 0, 10)
    oled.show()
    sleep_ms(1000)

    start_time = time.ticks_ms()
    x = 35  # Posición en X
    ante_y = 63 # Valor inicial de la posición y

    dibujarEjes(parametro)

    while time.ticks_diff(time.ticks_ms(), start_time) < 20000:  # 20 segundos
        # --- Lectura según parámetro ---
        if parametro == "luminosidad":
            valor_real = leerLuminosidadBinaria() # Porcetaje (0-100)
            escala_max = 100

        elif parametro == "temperatura":
            pin_04.measure()
            valor_real = mostrarTemperatura() # Unidad de medida = °C
            escala_max = 50

        elif parametro == "humedad":
            pin_04.measure()
            valor_real = mostrarHumedad() # Unidad de medida = %
            escala_max = 100
            
        # --- Rescalar dinámicamente ---
        valor = int((valor_real / escala_max) * 43)
        y = 63 - valor   # invertir para que valores altos suban

        # --- Graficar ---
        
        # --- Dibujar linea continua ---
        if x > 35:
            oled.line(x-1, ante_y, x, y, 1)
        ante_y = y
        
        # --- Reiniciar si se llena ---
        if x >= 127:
            dibujarEjes(parametro)
            x = 35
            ante_y = 63

        # Mostrar valor actual en la esquina superior derecha
        oled.fill_rect(80, 10, 48, 10, 0) # Limpiar zona
        oled.text(str(valor_real), 90, 10)
        
        if parametro == "temperatura":
            oled.text("C", 120, 10)
        elif parametro == "humedad" or parametro == "luminosidad":
            oled.text("%", 120, 10)
        
        oled.show()
        sleep_ms(200) # Muestra cada 0.2s
        x += 1 # Avanza 2px por lectura

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
        try:
            optn = input("Ingresa la opción que desees visualizar: ").strip()
            if optn.isdigit():
                optn = int(optn)
                if 1 <= optn <= 4:
                    if optn == 4:
                        oled.fill(0)
                        oled.text("Gracias", 36, 0)
                        oled.text("Por su atencion", 5, 10)
                        oled.show()
                        break
                    else:
                        menu(optn)
                        time.sleep(20)
                        desplegarMenu()
                else:
                    print("ERROR. Opción incorrecta")
                    oled.fill(0)
                    oled.text("ERROR.", 0,0)
                    oled.text('Opcion incorrecta', 0, 10)
                    oled.show()
                    desplegarMenu()
            else:
                print("Debes ingresar un numero entre (1-3)")
        except Exception as e:
            print("Error en: ", e)
