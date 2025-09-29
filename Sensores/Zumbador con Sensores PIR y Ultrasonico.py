"""
Integrantes:
    Rocha Sainez Jeshua Isaaac
    Becerra Quezada Fabricio
    
Fecha:
    29/09/2025

Proposito:
    Integración de los sensores: sensor de movimiento PIR y sensor ultrasonico
    junto con el actuador (zumbador activo o pasivo) para crear la función que
    marcará la distancia de los objetos detectados a su alrededor a través de un
    beep emitido por zumbador, y al detectar movimiento empiece a sonar una melodía
    personalizada por el zumbador. 

Objetivo:
    Mejorar el programa existente de sensores PIR y ultrasonido agregando
    funcionalidades adicionales mediante un zumbador. El objetivo es combinar
    la interacción de los sensores con una respuesta auditiva dinámica y una
    melodía personalizada.
"""

#Librerias a utilizar
from machine import PWM, Pin, SoftI2C
from hcsr04 import HCSR04
from time import sleep
import machine
import ssd1306
# Configuramos los pines y tiempo máximo de espera antes de producir un error
# del sensor ultrasonico para el microcontrolador
sensor_ultrasonico = HCSR04(trigger_pin=15, echo_pin=12, echo_timeout_us=10000)

# Configuración del sensor PIR
PIR_Interrupt = Pin(13, Pin.IN)

# Configuración de oled
i2cOled = SoftI2C(scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2cOled)

# Configuramos el pin y la frecuencia del zumbador
pin_zumbador = Pin(14)
pwm_zumbador = PWM(pin_zumbador, freq=440)

# Creamos la función para configurar el zumbador con el sensor ultrasonico
def marcar_distancia_con_zumbador():
    """
    Leer el ultrasónico para medir la distancia y
    emitir los beeps cuya frecuencia depende de la distancia
    """
    
    try:
        distancia = sensor_ultrasonico.distance_cm()
        
        # Validación de errores comunes en HCSR04
        if distancia in (250, -1, 0):
            print("ERROR: Lectura no válida")
        else:
            medida = distancia, "cm"
            print(medida)
            oled.fill(0)
            oled.text("Distacia: ", 0, 0)
            oled.text('d.d: {}'.format(distancia)+'cm', 0, 10)
            oled.show()
            # Encender beep corto
            pwm_zumbador.freq(1000) # Frecuencia fija de beep
            # Establecemos el ciclo de trabajo para generar el tono
            pwm_zumbador.duty(1023) # En pocas palabras se enciende
            sleep(0.05)
            pwm_zumbador.duty(0) # Apagamos
            
            # Definir retardos
            if distancia < 50:
                retardo = 0.1 # Retardo del beep, beep rapido
            else:
                """
                Calculamos el retardo proporcional para las distancia largas
                
                Punto inicial:
                Distancia > 50 cm → Retardo proporcional (ej: 0.5 segundos para 100 cm, 1 segundo para 200 cm, etc.).
                
                Por lo tanto la relación entre la distancia y el retardo es lineal: retardo = k * distancia
                k = constante de proporcionalidad
                
                Valor de la constante:
                --> Para 100 cm el retardo es de 0.5 segundos
                retardo = 0.5 -----> 0.5 = k * 100 ------> k = 0.5/100 ------> k = 0.005
                
                Equivalencia:
                retardo = 0.005 * 100 -----> retardo = 0.5
                
                Formulación:
                Por lo tanto deducimos que por cada 100 cm de distancia el retardo aumenta 0.5 segundos,
                ya que existe una relacion entre retardo y distancia ----> retardo / distancia
                
                y finalmente la formula quedaria de la siguiente manera
                
                          distancia
                retardo = --------- * 0.5
                            100
                
                como si una relación de 3 se tratará:           100 cm = 0.5 segundos
                                                      distancia medida = retardo
                """ 
                retardo = (distancia / 100) * 0.5
            
            sleep(retardo)
            
    except Exception as ex:
        print("Excepcion en:", ex)
        sleep(0.5)

# Creamos la función para configurar el zumbador con el sensor de movimiento PIR
def sonar_melodia_con_PIR():
    """
    Creamos la función para detectar movimiento y reproducimos una nota personalizada
    """
    
    """
    ¿Cómo funcionan las frecuencias para crear notas musicales?
    
    Teoria:
    Frecuencia = número de vibraciones por segundo
    Cada frecuancia emite un tono que nosotros percibimos como mas
    grave o agudo.
    
    Ejemplos: 100 Hz es un zumbido grave y lento, 1000 Hz es un beep agudo (otro zumbido)
              y 4000 Hz es un zumbido muy agudo, casi molesto.
    
    Melodía: es un cambio de frecuencia en una secuencia.
    Beep: es una secuencia fija por tiempo corto.
              
    Tabla de equivalencias entre notas y frecuencias:
    
    Nota              Frecuencia
    C4 (Do)           262 Hz
    D4 (Re)           294 Hz
    E4 (Mi)           330 Hz
    F4 (Fa)           349 Hz
    G4 (Sol)          392 Hz
    A4 (La)           440 Hz
    B4 (Si)           494 Hz
    
    C5 (Do')          523 Hz
    D5 (Re')          587 Hz
    E5 (Mi')          659 Hz
    F5 (Fa')          698 Hz
    G5 (Sol')         784 Hz
    A5 (La')          880 Hz
    B5 (Si')          988 Hz
    
    Método:
    Usamos el método PWM (Modulación por Ancho de Pulso) para enviar
    al buzzer una onda cuadrada  --> encendido/apagado rápido
    
    freq(x) --> define cuantas veces por segundo cambia entre alto y bajo,
    dando como resultado el tono.
    
    duty(x) --> define cuanto tiempo esta encedido/apagado en cada ciclo
    (sirve para controlar el volumen o intensidad)
    """
    
    # Creamos el diccionario de notas musicales (frecuencia para el zumbador en Hz)
    # usando solamente las notas que queremos para la canción
    notas = {
        "Do4": 262,
        "Re4": 294,
        "Mi4": 330,
        "Fa4": 349,
        "Sol4": 392,
        "La4": 440,
        "Si4": 494,
        "Do5": 523,
        "Re5": 587,
        "Mi5": 659,
        "Fa5": 698,
        "Sol5": 784,
        "La5": 880,
        "Si5": 988
        }
    
    """
    Organizamos las notas de acuerdo a la secuencia de la melodía,
    en este caso, nuestra melodía es de Zelda: Ocarina of Time.
    La secuencia esta inspirada en la melodía de un video tutorial
    para tocar esta melodía en una flauta
    """
    melodia = [("Fa4", 0.3), ("La4", 0.3), ("Si4", 0.3),
               ("Fa4", 0.3), ("La4", 0.3), ("Si4", 0.3),
               ("Fa4", 0.3), ("La4", 0.3), ("Si4", 0.3), ("Mi5", 0.5), ("Re5", 0.5),
               ("Si4", 0.3), ("Do5", 0.3), ("Si4", 0.4), ("Sol4", 0.4), ("Mi4", 0.7),
               ("Re4", 0.3), ("Mi4", 0.3), ("Sol4", 0.4), ("Mi4", 0.7),
               
               ("Fa4", 0.3), ("La4", 0.3), ("Si4", 0.3),
               ("Fa4", 0.3), ("La4", 0.3), ("Si4", 0.3),
               ("Fa4", 0.3), ("La4", 0.3), ("Si4", 0.3), ("Mi5", 0.5), ("Re5", 0.5),
               ("Si4", 0.3), ("Do5", 0.3), ("Mi5", 0.4), ("Si4", 0.4), ("Sol4", 0.7),
               ("Si4", 0.3), ("Sol4", 0.3), ("Re4", 0.4), ("Mi4", 0.7)]
    
    """
    Esta melodía contiene tiempos de duración (algunos mas largos que otros) para
    darle un ritmo a la melodía al momento de reproducirla, con el fin de que no se
    escuche tan robotizada.
    """
    
    if PIR_Interrupt.value() == 1: # Valor de movimiento detectado
        print("Movimiento detectado --> Reproduciendo melodía...")
        # Recorremos el ciclo para reproducir la frecuencia y mantenerla por cierto tiempo
        for nota, duracion in melodia:
            frecuencia = notas[nota] # Tomamos el valor de la nota
            pwm_zumbador.freq(frecuencia) # Agregamos la frecuencia
            pwm_zumbador.duty(800) # Hacemos sonar la nota
            sleep(duracion) # La hacemos sonar por un cierto tiempo
            pwm_zumbador.duty(0) # Detemos la nota para hacer una pausa
            sleep(0.05) # La mantenemos en pausa por un cierto tiempo

# Ciclo principal para usar los métodos
if __name__ == '__main__':
    while True:
        marcar_distancia_con_zumbador()
        sonar_melodia_con_PIR()
        
