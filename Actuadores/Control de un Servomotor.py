"""
Integrantes:
    Rocha Sainez Jeshua Isaaac
    Becerra Quezada Fabricio

Objetivo:
    Desarrollar una función en MicroPython que reciba como parámetro un ángulo
    (en grados) y controle un servomotor para que gire al ángulo especificado.
"""

from machine import Pin, PWM
from time import sleep

servo_pin = Pin(4, Pin.OUT)
servo_pwm = PWM(servo_pin)
servo_pwm.freq(50) # Frecuencia estándar para control de Servos (50Hz)

def insertar_angulo_servo(angulo):
    # Rango de valores PWM correspondientes es: 128 − 26 = 102.
    # El valor mínimo (26) es para desplazar el rango al nivel correcto
    duty_cycle = int(26 + (angulo / 125) * (128 - 26)) # Esto genera pulsos de entre 26 (0°) y 128 (125°)
    servo_pwm.duty(duty_cycle) # Acepta valores de 0 a 1023
    sleep(10) # Esperar a que se haga el movimiento
    
def pedir_angulo():
    try:
        # Ingresamos como el valor de ángulo como parametro personalizado
        angulo = int(input("Ingresar el angulo: "))
        # Rango de movimiento valido para el servomotor SG90
        if 0 <= angulo <= 125:
            insertar_angulo_servo(angulo)
        else:
            print("Angulo invalido, el rango valido es 0-125°")
    except Exception as ex:
        print("Error, solo se aceptan números enteros")
        
if __name__ == '__main__':
    while True:
        pedir_angulo()
        
    