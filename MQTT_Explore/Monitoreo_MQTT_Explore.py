# Implementación de librerias
from umqtt.simple import MQTTClient
from machine import Pin
from dht import DHT11
import network
import time

# Parametros de configuración Wi-Fi
ssid = "rochasainez"
password = "35631354"
# Parametros de configuración MQTT Explore
BROKER = "192.168.0.158"
Topic_Humedad = "proyecto/sensor_1/humedad"
Topic_Temperatura = "proyecto/sensor_2/temperatura"
Topic_Luminosidad = "proyecto/sensor_3/luminosidad"
Topic_LED = "proyecto/actuador/led"
mqtt_user = "Jeshua"
mqtt_password = "Jirs00924XY/"

# Configuración de la fotorresistencia
sensor_LDR = Pin(25, Pin.IN)
# Configuración de DHT11 (sensor para medir humedad y temperatura)
sensor_DHT = DHT11(Pin(4)) # crea el objeto pin_04 para un módulo DHT11 en el pin 04
# Configuración de PIN 2 para controlar la salida de la luz del LED
LED = Pin(2, Pin.OUT)

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

# Función de callback para manejar mensajes recibidos MQTT
def callback(topic, msg):
    # Mensaje de verificación para observar lo que el dispositivo esta recibiendo
    print("Mensaje recibido: ", topic, msg)
    if msg == b"ON":
        LED.value(1)
        print("LED = ON")
    else:
        LED.value(0)
        print("LED = OFF")

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

# Llamada a la función para la conexión de Wifi
conectar_Wifi(ssid, password)

try:
    # Crear cliente MQTT, con parámetros de seguridad para autenticarse y realizar la conexión
    cliente = MQTTClient("ESP32", BROKER, user=mqtt_user, password=mqtt_password)
    # Configurar función de callback para mensajes
    cliente.set_callback(callback)
    # Conectar al servidor MQTT
    cliente.connect()
    # Suscribirse al tema
    cliente.subscribe(Topic_LED)
    # Imprimir información de conexión
    print("Conectando cliente al Broker MQTT")
    print("Suscrito al tema: ", Topic_LED)
except Exception as ex:
    print("Error al conectar: ", ex)

# Bucle principal donde se realiza:
# la lectura de los sensores, publicar datos continuamente
# y mostrar mensajes entrantes de los actuadores
while True:
    sensor_DHT.measure()
    humedad = sensor_DHT.humidity()
    temperatura = sensor_DHT.temperature()
    luminosidad = leerLuminosidadBinaria()
    
    cliente.publish(Topic_Humedad, str(round(humedad, 2)))
    cliente.publish(Topic_Temperatura, str(round(temperatura, 2)))
    cliente.publish(Topic_Luminosidad, str(round(luminosidad, 2)))
    
    cliente.check_msg()
    time.sleep(2)
        