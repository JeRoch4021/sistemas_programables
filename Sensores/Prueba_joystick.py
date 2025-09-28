from machine import Pin, ADC, SoftI2C
from time import sleep_ms
import ssd1306

vrx = ADC(Pin(12, Pin.IN))
vry = ADC(Pin(13, Pin.IN))

vrx.atten(ADC.ATTN_11DB)
vry.atten(ADC.ATTN_11DB)

i2c = SoftI2C(scl=Pin(33), sda=Pin(32))
pin = Pin(16, Pin.OUT)
pin.value(0) # Configura GPIO16 en bajo para
resetear el OLED
pin.value(1) # Mientras que el OLED esté
ejecutándose, GPIO16 debe estar en 1
oled_ancho = 128 # Ancho de OLED
oled_alto = 64 # Alto de OLED
oled = ssd1306.SSD1306_I2C(oled_ancho,
oled_alto, i2c)
oled.fill(0)

def Map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min)*(out_max - out_min) / (in_max - in_min) + out_min)

while True:
    valorX = vrx.read()
    valorY = vry.read()
    
    posX = Map(valorX, 0, 4095, 0, 127)
    posY = Map(valorY, 0, 4095, 0, 63)
    print("X = ", posX, " Y = ", posY)
    oled.pixel(posX, posY, 1)
    
    oled.show()
    sleep_ms(100)
    
    
    