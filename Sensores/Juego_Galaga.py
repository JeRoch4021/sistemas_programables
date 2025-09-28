"""
Integrantes:
    Rocha Sainez Jeshua Isaaac
    Becerra Quezada Fabricio
    
Fecha:
    29/09/2025

Objetivo:
    Diseñar e implementar un juego interactivo en una pantalla OLED,
    utilizando el sensor MPU6050  y joystick como control de movimiento.
    El jugador deberá manipular un personaje o cursor en tiempo real
    mediante la inclinación del dispositivo, enfrentando desafíos dinámicos
    basados en la física del movimiento.
"""

from machine import Pin, ADC, SoftI2C
from time import sleep, ticks_ms, ticks_diff
from mpu6050 import MPU6050
import ssd1306
import urandom

# Configuracion de OLED
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Configuración de mpu
i2c_mpu = SoftI2C(scl=Pin(22), sda=Pin(21))
mpu = MPU6050(i2c_mpu)

# Configuración del Joystick
joy_x = ADC(Pin(26)) # Eje X
joy_y = ADC(Pin(27)) # Eje Y
joy_x.atten(ADC.ATTN_11DB)  # Extiende rango a 0-3.3 V
joy_y.atten(ADC.ATTN_11DB)
# Configuramos el botón SW del JoyStick 
btn_select = Pin(25, Pin.IN, Pin.PULL_UP)

# Puntuación y vidas del jugador
puntos = 0
vidas = 3
nivel = 1
# Programación de las balas disparadas por la nave
balas = []
vel_bala = 4
ultimo_disparo = 0
cooldown = 0.8     # Segundos entre ráfagas

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

ancho_alien = len(ICONO_ALIEN[0])
alto_alien = len(ICONO_ALIEN)

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
y = 60
velocidad_nave = 2 # Velocidad inicial de la nave
velocidad_enemigos = 1

def animacion_rapida(x_nave, y_nave):
    # Animación de energía alrededor de la nave
    for i in range(3):
        # Dibujar un borde parpadeante
        for dx in range(-2, ancho_nave+2):
            oled.pixel(x_nave + dx, y_nave - 1, 1)  # Arriba
            oled.pixel(x_nave + dx, y_nave + alto_nave, 1)  # Abajo
        for dy in range(-1, alto_nave+1):
            oled.pixel(x_nave - 2, y_nave + dy, 1)  # Izquierda
            oled.pixel(x_nave + ancho_nave + 1, y_nave + dy, 1)  # Derecha
        oled.show()
        sleep(0.05)
        # Borrar el borde
        for dx in range(-2, ancho_nave+2):
            oled.pixel(x_nave + dx, y_nave - 1, 0)
            oled.pixel(x_nave + dx, y_nave + alto_nave, 0)
        for dy in range(-1, alto_nave+1):
            oled.pixel(x_nave - 2, y_nave + dy, 0)
            oled.pixel(x_nave + ancho_nave + 1, y_nave + dy, 0)
        oled.show()
        sleep(0.05)

# Creamos la función para crear a los eneimgos y hacerlo aparecen en una
# área de la pantalla especifica
def crear_enemigos():
    enemigos = []
    for f in range(2):
        for c in range(4):
            # Diccionario de enmigos
            enemigos.append({"x":10+c*25, "y":10+f*15, "dir":1, "vivo":True})
    return enemigos

enemigos = crear_enemigos()

# Dibujar funciones
def dibujar_alien(x_pos, y_pos):
    for fila in range(alto_alien):
        for col in range(ancho_alien):
            if ICONO_ALIEN[fila][col] == 1:
                oled.pixel(x_pos + col, y_pos + fila, 1)

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
    if val_x < 1600:
        x -= velocidad_nave
    elif val_x > 2500:
        x += velocidad_nave

    # Movimiento vertical (invertido: arriba es menor)
    if val_y < 1600:
        y -= velocidad_nave
    elif val_y > 2500:
        y += velocidad_nave

    # Limitar dentro de los bordes de la pantalla
    if x < 0: x = 0
    if x > 128 - ancho_nave: x = 128 - ancho_nave
    if y < 10: y = 10
    if y > 64 - alto_nave: y = 64 - alto_nave

def mover_nave_mpu():
    global x, y
    datos = mpu.read_accel_data(g=False)
    ax = datos['x']
    ay = datos['y']

    # Ajustar sensibilidad (puedes cambiar los umbrales)
    if ax < -2:       # Inclinación a la izquierda
        y += 2
    elif ax > 2:      # Inclinación a la derecha
        y -= 2

    if ay > 2:        # Inclinación hacia adelante
        x -= 2
    elif ay < -2:     # Inclinación hacia atrás
        x += 2

    # Limitar los bordes de la pantalla
    if x < 0: x = 0
    if x > 128 - ancho_nave: x = 128 - ancho_nave
    if y < 10: y = 10
    if y > 64 - alto_nave: y = 64 - alto_nave
    
def mover_enemigos():
    for e in enemigos:
        if not e["vivo"]:
            continue
        e["x"] += e["dir"] * velocidad_enemigos
        if e["x"] <= 0 or e["x"] >= 128 - ancho_alien:
            e["dir"] *= -1
            e["y"] += 3
            
        # Si baja demasiado, reaparece arriba
        if e["y"] > 63 -alto_alien:
            e["y"] = 10
            e["x"] = urandom.getrandbits(7) % (128 - ancho_alien)

# Al detectar un movimiento rápido la nave hace una ráfaga de tres disparos
def power_up():
    global ultimo_disparo, x, y
    datos = mpu.read_accel_data(g=True)
    ax = abs(datos['x'])
    ay = abs(datos['y'])
    az = abs(datos['z'])

    # Detectar un "golpe rápido"
    if (ax > 1.0 or ay > 1.0 or az > 1.5) and ticks_diff(ticks_ms(), ultimo_disparo) > cooldown * 1000:
        ultimo_disparo = ticks_ms()
        animacion_rapida(x, y)# Animación especial del power_up
        # Ataque que especial: Triple ráfaga
        balas.append({"x": x + ancho_nave // 2, "y": y})
        balas.append({"x": x + ancho_nave // 2 - 2, "y": y})
        balas.append({"x": x + ancho_nave // 2 + 2, "y": y})
            
# Función para disparar cuando se presione el botón
def disparar():
    # Si el botón SW es presionado y hay menos de 3 balas en pantalla
    if not btn_select.value() and len(balas) < 3:
        balas.append({"x": x + ancho_nave//2, "y": y})
        sleep(0.1) # Anti-rebote simple para que no dispare demasiadas balas

def mover_balas():
    global balas
    for b in balas:
        b["y"] -= vel_bala
    balas = [b for b in balas if b["y"] > 0]

# Animación de explosión de la nave
def animar_explosion(x_e, y_e):
    for i in range(3):
        oled.fill_rect(x_e, y_e, ancho_alien, alto_alien, 1)
        oled.show()
        sleep(0.05)
        oled.fill_rect(x_e, y_e, ancho_alien, alto_alien, 0)
        oled.show()
        sleep(0.05)

# Función de colisiones
def detectar_colisiones():
    global balas, puntos, vidas, x, y
    nuevas_balas = []
    for b in balas:
        colision = False
        for e in enemigos:
            if e["vivo"]:
                # Colisiones bala-enemigo
                if (b["x"] >= e["x"] and b["x"] <= e["x"] + ancho_alien and
                    b["y"] >= e["y"] and b["y"] <= e["y"] + alto_alien):
                    e["vivo"] = False
                    puntos += 10
                    animar_explosion(e["x"], e["y"])
                    colision = True
                    break
        if not colision:
            nuevas_balas.append(b)
    balas[:] = nuevas_balas
    
    # Configuración del ciclo para las colisiones nave-enemigo
    for e in enemigos:
        if e["vivo"]:
            # Colisiones bala-enemigo
            if (x < e["x"] + ancho_alien and
                x + ancho_nave > e["x"] and
                y < e["y"] + alto_alien and
                y + alto_nave > e["y"]):
                vidas -= 1
                e["vivo"] = False # Enemigo destruido al chocar
                y += 10 # Empujar la nave hacia abajo
                if y > 64 - alto_nave:
                    y = 64 - alto_nave
                if vidas <= 0:
                    game_over()
    
def marcador():
    oled.text("p.p:{}".format(puntos), 0, 0)
    oled.text("v.v:{}".format(vidas), 85, 0)
    
"""
Creamos la función game_over para avisarle al jugador
que se ha quedado sin vidas para continuar con el juego,
por lo tanto regresará al incio del nivel
"""
def game_over():
    global puntos, nivel, vidas, balas, enemigos, x, y, velocidad_nave, velocidad_enemigos
    oled.fill(0)
    oled.text("GAME OVER", 30, 20)
    oled.text("p.p {}".format(puntos), 40, 40)
    oled.show()
    sleep(2)
    # Reiniciar juego
    puntos = 0
    vidas = 3
    nivel = 1
    velocidad_nave = 2
    velocidad_enemigos = 1
    balas.clear()
    x = (128 - ancho_nave) // 2
    y = 60
    enemigos = crear_enemigos()
    menu()

def presentar_nivel():
    global nivel
    oled.fill(0)
    oled.text("Next lvl {}".format(nivel), 25, 25)
    oled.show()
    sleep(2)
    oled.fill(0)
    
"""
Creamos la función verificar_nivel al momento de comprobar
que todos los enemigos hayan sido eliminados, para avanzar
al siguiente nivel en donde los enemigos van a reaparecer
pero con mayor velocidad.
"""
def pasar_siguiente_nivel():
    global enemigos, nivel, velocidad_nave, velocidad_enemigos, x, y
    if all(not e["vivo"] for e in enemigos):
        nivel += 1 # Avanzamos de nivel
        velocidad_nave += 1 # Aumentamos velocidad de la nave
        velocidad_enemigos += 1 # Aumentamos velocidad de los enemigos
        x = (128 - ancho_nave) // 2
        y = 60
        enemigos = crear_enemigos()
        presentar_nivel()

# Juego principal (joystick)
def ciclo_joystick():
    presentar_nivel()
    
    while True:
        oled.fill(0)
        
        mover_nave_joystick()
        disparar()
        power_up() # Detectar movimiento brusco y ejecutar power_up
        mover_enemigos()
        mover_balas()
        detectar_colisiones()
        pasar_siguiente_nivel()
        marcador()
        dibujar_nave(x, y)

        for e in enemigos:
            if e["vivo"]:
                dibujar_alien(e["x"], e["y"])

        for b in balas:
            oled.pixel(b["x"], b["y"], 1)

        oled.show()
        sleep(0.05)
    
def ciclo_mpu():
    presentar_nivel()
    
    while True:
        oled.fill(0)
        
        mover_nave_mpu() # Mover con inclinación
        disparar()
        power_up() # Detectar movimiento brusco y ejecutar power_up
        mover_enemigos()
        mover_balas()
        detectar_colisiones()
        pasar_siguiente_nivel()
        marcador()
        dibujar_nave(x, y)

        for e in enemigos:
            if e["vivo"]:
                dibujar_alien(e["x"], e["y"])

        for b in balas:
            oled.pixel(b["x"], b["y"], 1)

        oled.show()
        sleep(0.05)

# Menu principal para seleccionar el modo de movimiento
# Las opciones del menú se seleccionan con el joystick
def menu():
    opcion = 0
    opciones = ["Joystick", "MPU6050"]
    
    while True:
        oled.fill(0)
        oled.text("==Selecciona==", 8, 5)
        
        for i, texto in enumerate(opciones):
            # Flecha para resaltar opción seleccionada
            if i == opcion:
                oled.text("> " + texto, 15, 20 + i*15)
            else:
                oled.text("  " + texto, 15, 20 + i*15)
        
        oled.show()
        sleep(0.2)
        
        # Cambiar opción con inclinación del joystick
        val_y = joy_y.read()
        if val_y < 1600:
            opcion = 0        # Joystick
        elif val_y > 2500:
            opcion = 1        # MPU6050
        
        # Seleccionar al presionar botón
        if not btn_select.value():
            sleep(0.3)         # Anti-rebote
            if opcion == 0:
                ciclo_joystick()
            else:
                ciclo_mpu()
                
menu()
