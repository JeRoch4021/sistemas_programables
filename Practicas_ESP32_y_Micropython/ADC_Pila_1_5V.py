import machine
from time import sleep

# Configuración del pin ADC
pin_adc = machine.Pin(34) # Utilizamos el pin 34 para la lectura ADC
adc = machine.ADC(pin_adc) # Inicializamos el ADC en el pin seleccionado

# Configuración de la atenuación ATTN_2_5DB permite medir voltajes de hasta 1.5V
adc.atten(machine.ADC.ATTN_2_5DB)

# Por defecto, el ADC en MicroPython está configurado a 12 bits (0-4095) No es necesario cambiar la resolución en este caso

while True:
    valor_adc = adc.read() # Leer el valor bruto del ADC (0 - 4095)
    voltaje = valor_adc * (1.5 / 4095) # Convertir el valor ADC a voltaje Rango de 12 bits: 0 - 4095
    # Rango de voltaje con ATTN_2_5DB: 0.0V - 1.5V
    print("Valor ADC:", valor_adc, " - Voltaje:", round(voltaje, 2), "V") # Imprimir el valor ADC y el voltaje correspondiente
    sleep(1) # Esperar 1 segundo antes de la siguiente lectura
