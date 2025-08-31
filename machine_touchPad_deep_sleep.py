import machine, esp32

T0 = machine.TouchPad(machine.Pin(4))

T0.config(200) # Configura el umbral de reinicio (en el que el pin se considera tocado)

esp32.wake_on_touch(True)

print("El ESP32 entra en modo DEEP-SLEEP. Toca el GPIO04 para salir del modo DEEP-SLEEP.")

machine.deepsleep() # El ESP32 entra en modo LIGHT-SLEEP hasta que se toque el sensor