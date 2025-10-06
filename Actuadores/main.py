"""
Integrantes:
    Rocha Sainez Jeshua Isaaac
    Becerra Quezada Fabricio

Objetivo:
    Este archivo contiene el código principal del carrito. Aquí definimos los movimientos y su secuencia.
"""

from machine import Pin
import time
from ir_rx import NEC_16

# Pines del puente H 
IN1 = Pin(13, Pin.OUT) # Motor izquierdo
IN2 = Pin(12, Pin.OUT)
IN3 = Pin(14, Pin.OUT) # Motor derecho
IN4 = Pin(27, Pin.OUT)

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

# Funciones de movimiento
def avanzar():
    IN1.on(); IN2.off();
    IN3.on(); IN4.off();
    print("Avanzando")
    
def retroceder():
    IN1.off(); IN2.on();
    IN3.off(); IN4.on();
    print("Retrocediendo")
    
def girar_izquierda():
    IN1.off(); IN2.on();
    IN3.on(); IN4.off();
    print("Girar izquierda")
    
def girar_derecha():
    IN1.on(); IN2.off();
    IN3.off(); IN4.on();
    print("Girar derecha")
    
def detenerse():
    IN1.off(); IN2.off();
    IN3.off(); IN4.off();
    print("Detenido")
    

# CALLBACK IR
def callback_ir(data, addr, ctrl):
    """
    NEC_16 devuelve data de 16 bits
    """
    
    print("Boton IR recibido:", hex(data)) # Debug de consola
    
    # Navegación con flechas
    if data == codigos["UP"]:
        avanzar()
            
    elif data == codigos["DOWN"]:
        retroceder()
            
    elif data == codigos["LEFT"]:
        girar_izquierda()
        
    elif data == codigos["RIGHT"]:
        girar_derecha()
    
    elif data in (codigos["*"], codigos["#"]):
        detenerse()
    

# Iniciar receptor IR
ir = NEC_16(ir_pin, callback_ir)

print("Esperando códigos del control remoto...")

# Bucle principal
try:
    while True:
        time.sleep(0.1) # Mantenemos el programa vivo 
except KeyboardInterrupt:
    detenerse()
    print("Programa detenido manualmente")


