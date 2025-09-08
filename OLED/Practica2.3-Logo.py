'''
Integrantes del equipo:
Rocha Sainez Jeshua Isaac
Becerra Quezada Fabricio

Objetivo del programa:
Reemplazar el logotipo de Raspberry Pi por el logotipo del ITL
(Instituto Tecnológico de León) o del TecNM, cargándose como
una imagen en el formato adecuado (ejemplo .pbm) para finalmente
mostrarse en la pantalla OLED
'''

import machine
import ssd1306
import framebuf
from images import (LOGO) # Importar la matriz por medio de images.py almacenado en el microcontrolador

i2c = machine.SoftI2C(scl=machine.Pin(22), sda=machine.Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

buffer = bytearray(LOGO)
logo_tec = framebuf.FrameBuffer(buffer, 128, 64, framebuf.MONO_HLSB) # Convierte el formato de LOGO en binario

oled.fill(0)
# Logo del ITL ubicado en la esquina izquierda superior
oled.blit(logo_tec, 0, 0)
oled.show()
