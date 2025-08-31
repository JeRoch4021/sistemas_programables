from machine import Pin, TouchPad

T0 = TouchPad(Pin(4)); print("T0:", T0.read())

# O bien podemos usar ese circuito para reiniciar el ESP32 en modo light-sleep

import machine, esp32, time

T0 = machine.TouchPad(machine.Pin(4))

T0.config(200) # Configura el umbral de reinicio (en el que el pin se considera tocado)

esp32.wake_on_touch(True)

print("El ESP32 entra en modo LIGHT-SLEEP. Toca el GPIO04 para salir del modo LIGHTSLEEP.")

time.sleep_ms(10) # Retardo para que permita escribir el anterior texto antes de entrar en modo light-sleep

machine.lightsleep(); # El ESP32 entra en modo LIGHT-SLEEP

print("El ESP32 ha salido del modo LIGHT-SLEEP")
print("T0 =", T0.read()) # Imprime el valor de la capacitancia que ha provocado el reinicio