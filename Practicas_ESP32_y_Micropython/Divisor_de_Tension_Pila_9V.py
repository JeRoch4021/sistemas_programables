import machine
from time import sleep

pin34 = machine.Pin(34) # Se inicializa el PIN34
adc34 = machine.ADC(pin34) # Se inicializa la lectura ADC en el PIN34

# Configura la atenuación a 11 dB para medir hasta 3.3V
adc34.atten(machine.ADC.ATTN_11DB)

while True:
    # Lee el valor analógico del pin
    Volt = adc34.read() # Valor entre 0 y 4095 (12 bits)
    # Ajusta el valor leído para reflejar el voltaje real de la pila de 9V
    Volt_corregido = round(Volt / 4095 * 3.6 * (9.8 + 2) / 2, 2) # Ajuste según el divisor de voltaje
    # Imprime el voltaje corregido
    print("El voltaje es de:", Volt_corregido, "V")
    # Espera 5 segundos antes de la siguiente lectura
    sleep(5)
