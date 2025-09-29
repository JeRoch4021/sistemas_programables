"""
Integrantes:
    Rocha Sainez Jeshua Isaaac
    Becerra Quezada Fabricio
    
Fecha:
    29/09/2025

Objetivo:
    Desarrollar un programa que controle un foco de 110 V utilizando una fotocelda (LDR)
    como sensor de luz. Este proyecto te permitirá aprender cómo interactuar con sensores
    para tomar decisiones automáticas y controlar dispositivos eléctricos a través de
    programación.
"""

# Libreias a utilizar
from machine import Pin
import time

# Pin GPIO 25 para la entrada digital del LDR
LDR_PIN = Pin(25, Pin.IN) 

# Pin GPIO 27 para la salida del relévador
RELAY_PIN = Pin(27, Pin.OUT)

# Programa principal
while True:
        
        # Valor de LDR 0 igual a luz detectada
        if LDR_PIN.value() == 0:
            # Iluminado → apagar foco
            RELAY_PIN.value(0)
            print("Foco apagado (luz detectada)")
            
        # Valor de LDR 1 igual a luz perdida
        else:
            # Oscuro → encender foco
            RELAY_PIN.value(1)
            print("Foco encendido (oscuro)")
        # Realizamos una pausa por cada cambio de luz
        time.sleep(1)
