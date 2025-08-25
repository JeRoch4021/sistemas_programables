import machine

led_rojo=machine.Pin(2,machine.Pin.OUT)
led_rojo.on()

led_amarillo=machine.Pin(4,machine.Pin.OUT)
led_amarillo.on()

# Valores de led rojo
led_rojo.value(0)
led_rojo.value(True)
led_rojo.value(False)
led_rojo.value(True)

# Valores de led amarillo
led_amarillo.value(0)
led_amarillo.value(True)
led_amarillo.value(False)
led_amarillo.value(True)

import time

while True: #Error en la sintaxis de la palabra while
    
    # Secuencia del led rojo en 200 ms conectado al GPIO_04
    led_rojo.on()
    time.sleep(0.2)
    led_rojo.off()
    time.sleep(0.2)
    # Secuencia del led rojo en 200 ms conectado al GPIO_04
    led_rojo.on()
    time.sleep(0.2)
    led_rojo.off()
    time.sleep(0.2)
    
    # Secuencia del led amarillo en 500 ms conectado al GPIO_02
    led_amarillo.on()
    time.sleep(0.5)
    led_amarillo.off()
    time.sleep(0.5)
    
    