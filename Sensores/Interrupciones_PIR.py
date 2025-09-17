from machine import Pin
from time import sleep
Motion_Detected = False # Variable Global que contiene el estado del sensor de movimiento

def handle_interrupt(Pin): #Función de manejo de interrupciones
    global Motion_Detected
    Motion_Detected = True
    
led = Pin(14,Pin.OUT) # GPIO14 como salida (led)
PIR_Interrupt = Pin(13,Pin.IN) # GPIO13 como entrada (PIR)

# Adjuntar interrupción externa a GPIO13 y flanco ascendente como fuente de evento externo
PIR_Interrupt.irq(trigger = Pin.IRQ_RISING, handler = handle_interrupt)

while True:
    if Motion_Detected:
        print('Movimiento detectado!')
        led.value(1)
        sleep(20)
        led.value(0)
        print('Se detuvo el movimiento!')
        Motion_Detected = False
    else:
        led.value(1) # Led encendido
        sleep(1) # Retraso de 1 segundo
        led.value(0) # Led apagado
        sleep(1) # Retraso de 1 segundo