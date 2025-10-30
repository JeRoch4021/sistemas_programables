# Implementación de librerias
from machine import Pin, ADC
from dht import DHT11
import network
import urequests
import ujson
import time

# Parametros de configuración Wi-Fi
ssid = "rochasainez"
password = "35631354"
# Parametros de configuración ThingSpeak
Write_API_Key = "O7WDF0ANAL1CZREA"
Read_API_Key = "OZVCMXG8J3DPDJ0L"
channel_id = "3123961"
# Parametros de configuración TalkBack (Funcion que controla el LED desde ThingSpeak)
talkback_ID = "55553"
API_Key = "KGVK2VQVK9OC253H"
command_ID = "55006238"

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
    
    return wlan

# Método para mostrar en pantalla los valores de luminosidad durante 20 seg en la pantalla 
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

def leer_sensores():
    # Función para la lectura de los valores de los sensores y retornarlos a las URL del Broker
    try:
        sensor_DHT.measure()
        valor_humedad = sensor_DHT.humidity()
        valor_temperatura = sensor_DHT.temperature()
        valor_luminosidad = leerLuminosidadBinaria()
        return valor_humedad, valor_temperatura, valor_luminosidad
    except Exception as ex:
        print("Error en: ", ex)
        return None, None, None

# Llamada a la función para la conexión de Wifi
conectar_Wifi(ssid, password)

# Bucle infinito para leer sensores y actualizar ThingSpeak
while True:
    # Obtención de los valores de los sensores
    humedad, temperatura, luminosidad = leer_sensores()
    estado_LED_actual = LED.value()
    
    # Si alguno de los sensores falla, se salta el ciclo y vuelve a intentarlo
    # después de 10 segundos
    if humedad is None or temperatura is None or luminosidad is None:
        time.sleep(10)
        continue
    
    # Impresión de los resultados, como parte del diagnóstico
    print(f"Humedad: {humedad} % | Temperatura: {temperatura} °C | Luminosidad: {luminosidad} %")
    
    # Enviar datos a ThingSpeak (Field 1 = humedad, Field 2 = temperatura, Field 3 = luminosidad)
    url = f"https://api.thingspeak.com/update?api_key={Write_API_Key}&field1={humedad}&field2={temperatura}&field3={luminosidad}&field4={estado_LED_actual}"
    response = urequests.get(url)
    print("ThingSpeak: ", response.text)
    response.close()
    
    try:
        # URL para descargar todo el contenido del comando "ON" de TalkBack (proveniente de ThingSpeak)
        # para enceder el LED usando su Command_ID específico
        url_talkback = f"https://api.thingspeak.com/talkbacks/{talkback_ID}/commands/{command_ID}.json?api_key={API_Key}"
        response_TB = urequests.get(url_talkback)
        datos = response_TB.text
        response_TB.close()
        
        # Asignación del estado del LED inicial
        estado_LED = None
        # Convertir los datos json en un diccionario de texto de Python
        comando_json = ujson.loads(datos)
        # Extraer el valor del campo
        comando = comando_json["command_string"]
        print("Comando recibido: ", comando)
        
        # Lectura de los comandos recibidos,
        # los cuales usaremos para enceder y apagar el LED,
        # ademas de alternarlos con el fin de hacer que este
        # proceso sea automático y no manual.
        if comando:
            if comando == "ON":
                estado_LED = 1
                LED.value(estado_LED)
                command_ID = "55006239"
                print("LED = ON")
            elif comando == "OFF":
                estado_LED = 0
                LED.value(estado_LED)
                command_ID = "55006238"
                print("LED = OFF")
            # Si el comando no es conocido
            else:
                print("Comando invalido")
        # Si no se ha recibido comandos (cadena vacía)  
        else:
            print("TalkBack: Sin comandos nuevos")
    
    except Exception as ex:
        print("Error leyendo TalkBack: ", ex)
    
    time.sleep(20) # Espera minima entre actualizaciones    