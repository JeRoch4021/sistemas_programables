# Implementación de librerias
import network
import time
from machine import UART
from umqtt.simple import MQTTClient

# Parámetros de configuración Wi-Fi
ssid = "rochasainez"
password = "35631354"

# Parámetros de configuración MQTT Dash
broker_MQTT = "broker.hivemq.com"
Topic_Latitud = b"practica/gps/latitud"
Topic_Longitud = b"practica/gps/longitud"
Topic_Altitud = b"practica/gps/altitud"
Topic_Velocidad = b"practica/gps/velocidad"

# Parámetros de configuración GPS
sensor_gps = UART(2, baudrate=9600, tx=13, rx=15, timeout=1000)

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

def convertir_grados(valor, direccion):
    """
    Convierte las coordenadas GPS del formato NMEA (DDMM.MMMM)
    a un formato decimal normal para que los mapas puedan entenderlo
    DD -> grados enteros
    MM.MMMM -> minutos decimales
    """
    try:
        # Revisamos que el valor no este vacio
        if not valor or valor == "":
            return None
        # Toma los primero dos o tres digitos y los
        # convierte a grados enteros
        grados = int(float(valor) / 100)
        # Extrae los miutos (la parte decimal después de los grados)
        minutos = float(valor) - grados * 100
        # Convertir los minutos a grados decimales
        decimal = grados + minutos / 60
        # Cambia el signo porque estas coordenadas son negativas
        if direccion is ['S', 'W']:
            decimal = -decimal
        return decimal
    except:
        return None

def parsear_linea(linea):
    """
    Esta función interpreta las tramas NMEA del modulo GPS y extrae
    de ellas los datos importantes (latitud, longitud, altitud y velocidad)
    """
    if linea.startswith("$GPGGA"):
        # Divide el texto en comas y crea una lista
        partes = linea.split(',')
        # Extracción de los datos específicos
        latitud = convertir_grados(partes[2], partes[3])
        longitud = convertir_grados(partes[4], partes[5])
        altitud = partes[9]
        return latitud, longitud, altitud
    if linea.startswith("$GPVTG"):
        try:
            # Divide el texto en comas y crea una lista
            partes = linea.split(',')
            # Extracción de los datos específicos
            velocidad = partes[7] if partes[7] != "" else 0.0 # Km/h
            return velocidad
        except Exception as ex:
            print("Error al parsear velocidad: ", ex)
            return "0.0"
    return None

def main():
    # Crear cliente MQTT
    cliente = MQTTClient("ESP32", broker_MQTT)
    # Conectar al servidor MQTT
    cliente.connect()
    # Imprimir información de conexión
    print("Conectando cliente al Broker MQTT: ", broker_MQTT)
    
    # Bucle infinito para leer continuamente los datos del sensor GPS,
    # procesar los datos (latitud, longitud, altitud y velocidad) y
    # enviar (por medio del Wifi) los datos al servidor MQTT para reflejarlos
    # en la aplicación MQTT Dash
    while True:
        # Leer la linea de texto enviada por el sensor GPS
        linea = sensor_gps.readline()
        # Se verifica que no haya una linea vacia
        if linea:
            try:
                # Convetir los bytes recibidos a texto legible y elimina
                # los saltos de linea o espacio sobreantes
                linea = sensor_gps.readline().decode("utf-8").strip()
                if linea.startswith("$GPGGA"):
                    # Recibimos los valores retornados para traducir
                    # las coordenadas al formato decimal
                    # (en este caso: latitud, longitud, altitud)
                    latitud, longitud, altitud = parsear_linea(linea)
                    if latitud and longitud:
                        # Impresión para verificar que los valores sean correctos
                        print("Latitud: ", latitud, "Longitud: ", longitud, "Altitud: ", altitud)
                        # Publicación de los datos al servidor MQTT
                        cliente.publish(Topic_Latitud, str(latitud))
                        cliente.publish(Topic_Longitud, str(longitud))
                        cliente.publish(Topic_Altitud, str(altitud))
                # Velocidad
                elif linea.startswith("$GPVTG"):
                    # Recibimos los valores al igual que la condición anterior
                    # (en este caso: velocidad)
                    velocidad = parsear_linea(linea)
                    print("Velocidad: ", velocidad, "Km/h")
                    # Publicación de los datos al servidor MQTT
                    cliente.publish(Topic_Velocidad, str(velocidad))
            except Exception as ex:
                print("Error en: ", ex)
        time.sleep(0.2)

# Función para ejecutar las principales funciones del programa final
if __name__ == '__main__':
    conectar_Wifi(ssid, password)
    main()