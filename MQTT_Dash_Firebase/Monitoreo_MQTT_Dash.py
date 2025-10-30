# Implementación de librerias
from umqtt.simple import MQTTClient
from machine import Pin, PWM
from dht import DHT11
import urequests
import machine
import network
import time

# Parámetros de configuración Wi-Fi
ssid = "rochasainez"
password = "35631354"

# Parámetros de configuración MQTT Dash
Address = "broker.hivemq.com"
Topic_Humedad = b"proyecto/sensor_1/humedad"
Topic_Temperatura = b"proyecto/sensor_2/temperatura"
Topic_Luminosidad = b"proyecto/sensor_3/luminosidad"
Topic_LED = b"proyecto/actuador_1/led"
Topic_Zumbador = b"proyecto/actuador_2/zumbador"

# Parámetro de configuración Firebase
Firebase_URL = "https://sistemasprogramables-14d0c-default-rtdb.firebaseio.com/.json"

# Configuración de la fotorresistencia
sensor_LDR = Pin(25, Pin.IN)
# Configuración de DHT11 (sensor para medir humedad y temperatura)
sensor_DHT = DHT11(Pin(4)) # crea el objeto pin_04 para un módulo DHT11 en el pin 04
# Configuración de PIN 2 para controlar la salida de la luz del LED
LED = Pin(2, Pin.OUT)
# Variable global para controlar la entrada de datos de Firebase para el led
Boolean_LED = False
# Configuramos el pin del zumbador
zumbador = PWM(Pin(14))
zumbador.duty(0)
# Variable global para controlar la entrada de datos de Firebase para el zumbador
Boolean_Zumbador = False

def conectar_Wifi(ssid, password):
    """
    Función para conectarse a una red Wi-Fi.
    :param ssid: Nombre de la red Wi-Fi
    :param password: Contraseña de la red Wi-Fi
    :return: Dirección IP asignada al dispositivo
    """
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    print("Conectando a la red Wifi...")
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(0.5)
        
    print("\nConexion exitosa")
    print("Direccion asignada", wlan.ifconfig()[0])

# Función para enviar los datos a la base de datos de Firebase
# Tomando como parámetros los valores medidos por los sensores y el resultado
# de los actuadores
def enviar_datos_firebase(humedad, temperatura, luminosidad, led, zumbador):
    # Diccionario de datos en forma de estructura anidada para luego convertirla
    # en un formato JSON para enviar a Firebase (el fin es organizar datos de forma clara)
    datos = {
        "Actuadores": {
            "Led": led,
            "Zumbador": zumbador
        },
        "Sensores": {
            "DHT": {
                "Humedad": humedad,
                "Temperatura": temperatura
            },
            "LDR": luminosidad
        } 
    }
    
    try:
        # Actualizamos solo las claves que se envian dentro del formato JSON
        response = urequests.patch(Firebase_URL, json=datos)
        # Mensaje de verificación para comprobar que los datos se enviaron correctamente
        print("Sensores enviados: ", response.status_code)
        # Cerramos la conexión para liberar memoria de microcontrolador
        response.close()
    except Exception as ex:
        print("Error al enviar sensores: ", ex)

# Función de callback para manejar mensajes recibidos MQTT
def mensaje_devuelto(topic, msg):
    # Variables globales para modificar sus valores dentro de la función
    global Boolean_LED, Boolean_Zumbador
    # Mensaje de verificación para observar lo que el dispositivo esta recibiendo
    print("Mensaje recibido: ", msg)
    if msg == b"led_1":
        LED.value(1)
        Boolean_LED = True
    elif msg == b"led_0":
        LED.value(0)
        Boolean_LED = False
    elif msg == b"buz_1":
        # Definimos una frecuencia de 1000 Hz para que se un tono audible
        zumbador.freq(1000)
        # Ajuste del ciclo de trabajo de la señal PWM
        zumbador.duty(512)
        Boolean_Zumbador = True
    else:
        zumbador.duty(0) # Apagamos el zumbador
        Boolean_Zumbador = False
     

# Método para mostrar en pantalla los valores de luminosidad durante 0.5 seg en la pantalla 
def mostrarLuminosidad():
    luminosidad = sensor_LDR.value()
    return luminosidad

def leerLuminosidadBinaria():
    # Devuelve el porcentaje aproximado de luminosidad usando el pin DO
    conteo = 0
    muestras = 10
    for _ in range(muestras):
        conteo += 1 - mostrarLuminosidad() # Ahora es solo 0 o 1
        time.sleep(0.5) # Leer cada medio segundo (0.5 segundos)
    porcentaje = int ((conteo/muestras)*100) # Porcentaje según la iluminosidad
    return porcentaje

# Función principal para establecer conexión MQTT
def escuchar_cliente():
    # Crear cliente MQTT
    cliente = MQTTClient("ESP32", Address, keepalive=10000)
    # Configurar función de callback para mensajes
    cliente.set_callback(mensaje_devuelto)
    # Conectar al servidor MQTT
    cliente.connect()
    # Suscribirse al tema
    cliente.subscribe(Topic_LED)
    cliente.subscribe(Topic_Zumbador)
    # Imprimir información de conexión
    print("Conectando cliente al Broker MQTT: ", Address)
    print("Suscrito al tema: ", Topic_LED)
    print("Suscrito al tema: ", Topic_Zumbador)
    try:
        # Bucle para leer sensores, mostrar valores para realizar un diagnóstico,
        # enviar datos a la base de datos de Firebase, publicar datos continuamente
        # y mostrar mensajes entrantes de los actuadores
        while True:
            sensor_DHT.measure()
            humedad = sensor_DHT.humidity()
            temperatura = sensor_DHT.temperature()
            luminosidad = leerLuminosidadBinaria()
            
            # Impresión de los resultados, como parte del diagnóstico
            print(f"Humedad: {humedad} % | Temperatura: {temperatura} °C | Luminosidad: {luminosidad} %")
            
            # Llamamos a la función para obtener los datos y registrarlos a la base de datos de Firebase
            enviar_datos_firebase(humedad, temperatura, luminosidad, Boolean_LED, Boolean_Zumbador)
            
            cliente.publish(Topic_Humedad, str(humedad))
            cliente.publish(Topic_Temperatura, str(temperatura))
            cliente.publish(Topic_Luminosidad, str(luminosidad))
    
            cliente.check_msg()
    finally:
        # Desconectar cliente MQTT
        cliente.disconnect()
        print("Cliente MQTT desconectado.")

# Función para ejecutar las principales funciones del programa final
if __name__ == '__main__':
    conectar_Wifi(ssid, password)
    escuchar_cliente()