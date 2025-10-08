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

# Motor izquierdo
IN1 = Pin(13, Pin.OUT)
IN2 = Pin(12, Pin.OUT)

# Motor derecho
IN3 = Pin(14, Pin.OUT)
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
    # Configuramos las salidas digitales para establecer la dirección hacia el norte,
    # es decir, moverse hacia adelante, usando UP del control remoto.
    IN1.off(); IN2.on();
    IN3.off(); IN4.on();
    print("Avanzando")
    
def retroceder():
    # Configuramos las salidas digitales para establecer la dirección hacia el sur,
    # es decir, moverse hacia atrás, usando DOWN del control remoto.
    IN1.on(); IN2.off();
    IN3.on(); IN4.off();
    print("Retrocediendo")
    
def girar_izquierda():
    # Configuramos las salidas digitales para establecer la dirección hacia el oeste,
    # es decir, moverse hacia la izquierda, usando LEFT del control remoto.
    IN1.off(); IN2.on();
    IN3.on(); IN4.off();
    print("Girar izquierda")
    
def girar_derecha():
    # Configuramos las salidas digitales para establecer la dirección hacia el este,
    # es decir, moverse hacia la derecha, usando RIGHT del control remoto.
    IN1.on(); IN2.off();
    IN3.off(); IN4.on();
    print("Girar derecha")
    
def detenerse():
    # Configuramos las salidas digitales para establecer el freno,
    # es decir, que pare de moverse, usando * o # (cualquiera de los dos hace lo mismo) del control remoto.
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


