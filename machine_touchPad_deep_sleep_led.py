from machine import Pin, TouchPad
import time

T0 = TouchPad(Pin(4));
LED2 = Pin(2, mode=Pin.OUT, value=0) # se inicializa el GPIO2 como salida del LED interno y se deja apagado

tiempoLimite = time.ticks_add(time.ticks_ms(), 100) # se define la variable tiempoLimite para comprobar T0 tiempo RTC + 100 ms

while True:
    if time.ticks_diff(tiempoLimite, time.ticks_ms()) <= 0: # se compruebas si el tiempoLimite se ha agotado
        if T0.read() < 300: # si el tiempo se ha agotado y T0 tiene contacto...
            LED2.on() # ... se enciende el LED
        else: # si el tiempo se ha agotado y T0 no tiene contacto...
            LED2.off() # ...se apaga el LED
        tiempoLimite = time.ticks_add(time.ticks_ms(), 100) # nuevo tiempoLimite (tiempo RTC + 100 ms)