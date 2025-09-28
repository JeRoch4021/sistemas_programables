from machine import Pin, ADC, SoftI2C
from time import sleep
from mpu6050 import MPU6050
import ssd1306

# Configuracion de OLED
i2c = SoftI2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306(128, 64, i2c)

# Configuración de mpu
i2c_mpu = SoftI2C(scl=Pin(22), sda=Pin(21))
mpu = MPU6050(i2c_mpu)

# Configuración del Joystick
joy_x = ADC(Pin(26)) # Eje X
joy_y = ADC(Pin(27)) # Eje Y
joy_x.atten(ADC.ATTN_11DB)  # Extiende rango a 0-3.3 V
joy_y.atten(ADC.ATTN_11DB)

# Puntuación y vidas del jugador
puntos = 0
vidas = 3

ICONO_ALIEN = [ # Matriz de alien (enemigo)
    [0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0],
    [1, 1, 0, 0, 1, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1],
]

ancho_alien = len(ICONO_ENEMIGO[0])
alto_alien = len(ICONO_ENEMIGO)

enemigos = []
for f in range(2):
    for c in range(4):
        # Diccionario de enmigos
        enemigos.append({"x":10+c*25, "y":5+f*15, "dir":1, "vivo":True})

def dibujar_alien(x_pos, y_pos):
    for fila in range(alto_alien):
        for col in range(ancho_alien):
            if ICONO_ALIEN[fila][col] == 1:
                oled.pixel(x_pos + col, y_pos + fila, 1)

def mover_enemigos():
    for e in enemigos:
        if not e["vivo"]:
            continue
        e["x"] += e["dir"]
        if e["x"] <= 0 or e["x"] >= 128 - ancho_alien:
            e["dir"] *= -1
            e["y"] += 3

ICONO_NAVE = [ # Matriz de la nave ()
    [0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 1, 1, 0, 1, 1, 0, 0],
    [0, 1, 1, 0, 0, 0, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 1, 1, 1, 0, 1, 1],
    [1, 0, 0, 1, 0, 1, 0, 0, 1],
    [0, 0, 0, 1, 0, 1, 0, 0, 0],
]

ancho_nave = len(ICONO_NAVE[0])
alto_nave = len(ICONO_NAVE)

# Posicion inicial de la nave
x = (128 - ancho_nave) // 2
y = (64 - alto_nave) // 2
velocidad = 2 # Velocidad inicial de la nave

# Método para dibujar la nave en la oled
def dibujar_nave(x_pos, y_pos):
    for fila in range(alto_nave):
        for col in range(ancho_nave):
            if ICONO_NAVE[fila][col] == 1:
                oled.pixel(x_pos + col, y_pos + fila, 1)

# Método para mover la nave
def mover_nave_joystick():
    global x, y
    val_x = joy_x.read() # 0 - 4095
    val_y = joy_y.read()

    # Movimiento horizontal
    if val_x < 1800:
        x -= velocidad
    elif val_x > 2300:
        x += velocidad

    # Movimiento vertical (invertido: arriba es menor)
    if val_y < 1800:
        y -= velocidad
    elif val_y > 2300:
        y += velocidad

    # Limitar dentro de los bordes de la pantalla
    if x < 0: x = 0
    if x > 128 - ancho_nave: x = 128 - ancho_nave
    if y < 0: y = 0
    if y > 64 - alto_nave: y = 64 - alto_nave

def mover_nave_mpu():
    global x, y
    datos = mpu.get_values()
    ax = datos['AcX']
    ay = datos['AcY']

    # Ajustar sensibilidad (puedes cambiar los umbrales)
    if ax < -2000:       # Inclinación a la izquierda
        x -= 2
    elif ax > 2000:      # Inclinación a la derecha
        x += 2

    if ay > 2000:        # Inclinación hacia adelante
        y += 2
    elif ay < -2000:     # Inclinación hacia atrás
        y -= 2

    # Limitar los bordes de la pantalla
    if x < 0: x = 0
    if x > 128 - ancho_nave: x = 128 - ancho_nave
    if y < 0: y = 0
    if y > 64 - alto_nave: y = 64 - alto_nave

ultimo_disparo = 0
cooldown = 0.8     # Segundos entre ráfagas

# Al detectar un movimiento rápido la nave hace una ráfaga de tres disparos
def disparo_rafaga():
    global ultimo_disparo
    datos = mpu.get_values()
    ax = abs(datos['AcX'])
    ay = abs(datos['AcY'])
    az = abs(datos['AcZ'])

    # Detectar un "golpe rápido"
    if (ax > 12000 or ay > 12000 or az > 20000) and (time.ticks_ms() - ultimo_disparo > cooldown * 1000):
        ultimo_disparo = time.ticks_ms()
        # Generar tres balas con un pequeño retraso
        for i in range(3):
            balas.append({"x": x + ANCHO_NAVE // 2, "y": y})
            time.sleep(0.1)   # 100ms entre balas

# Programación de las balas disparadas por la nave
balas = []
vel_bala = 4

def mover_balas():
    global balas
    for b in balas:
        b["y"] -= vel_bala
    balas = [b for b in balas if b["y"] > 0]

def disparar():
    if not btn.value() and len(balas) < 3:
        balas.append({"x": x + ANCHO_NAVE//2, "y": y})

def detectar_colisiones():
    global balas
    nuevas_balas = []
    for b in balas:
        colision = False
        for e in enemigos:
            if e["vivo"]:
                if (b["x"] >= e["x"] and b["x"] <= e["x"] + ANCHO_ALIEN and
                    b["y"] >= e["y"] and b["y"] <= e["y"] + ALTO_ALIEN):
                    e["vivo"] = False
                    puntos += 10
                    colision = True
                    break
        if not colision:
            nuevas_balas.append(b)
    balas = nuevas_balas
    
def marcador():
    oled.text("Puntos {}".format(puntos), 0, 0)
    oled.text("Vidas {}".format(vidas), 80, 0)

# Juego principal (joystick)
def ciclo_joystick():
    while True:
        oled.fill(0)
        
        mover_nave_joystick()
        disparo_rafaga()
        
        mover_enemigos()
        disparar()
        mover_balas()
        detectar_colisiones()
        
        marcador()
        dibujar_nave(x, y)

        for e in enemigos:
            if e["vivo"]:
                dibujar_alien(e["x"], e["y"])

        for b in balas:
            oled.pixel(b["x"], b["y"], 1)

    oled.show()
    time.sleep(0.05)
    
def ciclo_mpu():
    while True:
        oled.fill(0)

        mover_nave_mpu()          # Mover con inclinación
        disparo_rafaga()          # Detectar movimiento rápido y disparar

        mover_enemigos()
        disparar()
        mover_balas()
        detectar_colisiones()

        marcador()
        dibujar_nave(x, y)

        for e in enemigos:
            if e["vivo"]:
                dibujar_alien(e["x"], e["y"])

        for b in balas:
            oled.pixel(b["x"], b["y"], 1)

        oled.show()
        time.sleep(0.05)

# Menu principal para seleccionar el modo de movimiento
# Las opciones del menú se seleccionan con el joystick
def menu():
    opcion = 0
    opciones = ["Joystick", "MPU6050"]
    
    while True:
        oled.fill(0)
        oled.text("== Selecciona ==", 10, 5)
        
        for i, texto in enumerate(opciones):
            # Flecha para resaltar opción seleccionada
            if i == opcion:
                oled.text("> " + texto, 10, 20 + i*15)
            else:
                oled.text("  " + texto, 10, 20 + i*15)
        
        oled.show()
        sleep(0.2)
        
        # Cambiar opción con inclinación del joystick
        val_y = joy_y.read()
        if val_y < 1800:
            opcion = 0        # Joystick
        elif val_y > 2300:
            opcion = 1        # MPU6050
        
        # Seleccionar al presionar botón
        if not btn_select.value():
            sleep(0.3)         # Anti-rebote
            if opcion == 0:
                ciclo_joystick()
            else:
                ciclo_mpu()
                
menu()
