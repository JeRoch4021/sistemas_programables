from machine import Pin, ADC, SoftI2C
import ssd1306
import time

# Código de pantalla oled
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c) # Pantalla de 128x64 píxeles

# Configurar el sensor LDR
ldr = Pin(25, Pin.IN)

while True:
    valor = ldr.value() # Leer el valor del sensor (0-4095)
    print("Luz detectada:", valor) # Mostrar en la terminal
    
    oled.fill(0) # Limpiar la pantalla y actualizar datos
    oled.text("Sensor LDR", 20, 5)
    
    if valor == 0:
        oled.text("Luz alta:", 25, 25)
        oled.text(str(valor), 60, 45)
    else:
        oled.text("Luz baja:", 25, 25)
        oled.text(str(valor), 60, 45)
        
    oled.show()
    time.sleep(0.5) # Esperar medio segundo