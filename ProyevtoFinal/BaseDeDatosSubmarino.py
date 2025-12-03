import network
import machine
from dht import DHT11
from mpu6050 import MPU6050
import urequests
import ujson
import time

# Configuración de wifi
ssid = "" # Cambiar
password = "" # Cambiar

# Configuracion de pines para la lectura de sensores
# Sensor de temperatura
pin_04 = DHT11(machine.Pin(4))
# Sensor MPU6050
i2c = machine.SoftI2C(scl=machine.Pin(22), sda=machine.Pin(21))
mpu = MPU6050(i2c)

# Configuracion de Firestore
api_key = "AIzaSyB5zkjJg_j3w0b28J3NJolgkKqzQKnX9mg"
project_id = "submarino-iot"

# Colección donde se guardarán los datos
coleccion = "lecturas"

# Conexión WiFi
def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    print("Conectando a WiFi...")
    while not wlan.isconnected():
        time.sleep(0.5)
        print(".", end="")

    print("\nWiFi conectado:", wlan.ifconfig())

# Lee los datos del sensor MPU
def leerDatosMPU():
    ax, ay, az, gx, gy, gz = mpu.get_values()
    datos = {ax, ay, az, gx, gy, gz}
    return datos

# Lee los datos del sensor de temperatura
def leerTempertura():
    pin_04.measure()
    temp = pin_04.temperature() 
    humedad = pin_04.humidity()
    return temp, humedad

# Enviar datos a Firestore
def enviar_firestore(data):
    
    # URL para enviar los datos a Firestore
    url = (
        "https://firestore.googleapis.com/v1/projects/"
        + project_id
        + "/databases/(default)/documents/"
        + coleccion
        + "?key="
        + api_key
    )

    # Formato especial para Firestore:
    payload = {
        "fields": {
            "timestamp": {"stringValue": str(time.time())},

            "temperatura": {"doubleValue": data["temperatura"]},
            "humedad": {"doubleValue": data["humedad"]},
            
            #"ph": {"doubleValue": data["ph"]},

            "accel_x": {"doubleValue": data["ax"]},
            "accel_y": {"doubleValue": data["ay"]},
            "accel_z": {"doubleValue": data["az"]},

            "gyro_x": {"doubleValue": data["gx"]},
            "gyro_y": {"doubleValue": data["gy"]},
            "gyro_z": {"doubleValue": data["gz"]},
        }
    }

    headers = {"Content-Type": "application/json"}

    try:
        resp = urequests.post(url, data=ujson.dumps(payload), headers=headers)
        print("Firestore respuesta:", resp.text)
        resp.close()
    except Exception as e:
        print("Error enviando:", e)


conectar_wifi()

# Ciclo de lectura de los datos
while True:
    # Datos de prueba
    """
    datos = {
        "temperatura": 23.5,
        "humedad": 10.00,
        "ph": 7.1,
        "ax": 0.12,
        "ay": -0.05,
        "az": 9.80,
        "gx": 0.01,
        "gy": -0.02,
        "gz": 0.00,
    }
    """
    
    datosMPU = leerDatosMPU()
    temp, hum = leerTemperatura()
    
    datos={
        "temperatura": temp,
        "humedad": hum,
        "ph": 7.1,  # Cambiar cuando haya oportunidad de usr el submarino
        "ax": datosMPU[0],
        "ay": datosMPU[1],
        "az": datosMPU[2],
        "gx": datosMPU[3],
        "gy": datosMPU[4],
        "gz": datosMPU[5],
        
        """
        # Datos de prueba
        "ax": 0.12,
        "ay": -0.05,
        "az": 9.80,
        "gx": 0.01,
        "gy": -0.02,
        "gz": 0.00,
        """
    }
    

    enviar_firestore(datos)
    time.sleep(5)
