import network # Para conectarse a Wi-Fi
import socket # Para crear un servidor web
import time # Para manejar pausas
from acamera import Camera, FrameSize, PixelFormat

# Configuración de la camara 
cam = Camera(frame_size=FrameSize.QQVGA, pixel_format=PixelFormat.JPEG, jpeg_quality=85, init=False)

# Configuración de la red
ssid = "rochasainez"
password = "35631354"

def conectar_wifi(ssid, password):
    """
    Función para conectarse a una red Wi-Fi.
    :param ssid: Nombre de la red Wi-Fi
    :param password: Contraseña de la red Wi-Fi
    :return: Dirección IP asignada al dispositivo
    """
    wlan = network.WLAN(network.STA_IF)
    # Configurar la interfaz de red
    wlan.active(True) # Activar la interfaz
    # Conectar a la red Wi-Fi
    wlan.connect(ssid, password)
    
    print("Conectando a la red Wi-Fi...")
    while not wlan.isconnected(): # Esperar hasta que se establezca la conexión
        time.sleep(1)
        print('.', end='') # Mostrar puntos para indicar que se está intentando conectar
    
    print("\n¡Conexión exitosa!")
    print("Dirección IP asignada:", wlan.ifconfig()[0]) # Mostrar la dirección IP
    return wlan.ifconfig()[0] # Retornar la dirección IP

# Inicializar camara
def inicializar_camara():
    try:
        cam.init()
        time.sleep(1)
        print("Camara inicializada correctamente.")
    except Exception as ex:
        print('Error al inicializar la cámara:', ex)                

# Función para enviar foto
def enviar_foto(conn):
    try:
        frame = cam.capture()
        with open('imagen.jpg', 'wb') as abrir_imagen:
            abrir_imagen.write(frame)
        conn.send(b'HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\n\r\n')
        conn.send(frame)
    except Exception as ex:
        print("Error al capturar imagen: ", ex)
        conn.send(b"HTTP/1.1 500 Internal Server Error\r\n\r\n")

# Función para enviar streaming
def enviar_stream(conn):
    try:
        conn.send(b'HTTP/1.1 200 OK\r\nContent-Type: multipart/x-mixed-replace; boundary=frame\r\n\r\n')
        while True:
            frame = cam.capture()
            conn.send(b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.1)
    except Exception as ex:
        print("Streaming detenido: ", ex)


def iniciar_servidor(ip):
    addr = (ip, 80) # Dirección IP y puerto del servidor (puerto 80 es estándar para HTTP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Crear un socket TCP/IP
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Reutiliza la dirección
    s.bind(addr) # Enlazar el socket a la dirección IP y puerto
    s.listen(5)
    print('Servidor web iniciado en http://%s:80' % ip)
    
    while True:
        conn, addr = s.accept()
        print('Conexión desde:', addr)
        try:
            request = conn.recv(1024).decode() # Recibir la solicitud del cliente
            print('Solicitud recibida:', request)
            
            if "GET /foto" in request:
                enviar_foto(conn)
            elif "GET /stream" in request:
                enviar_stream(conn)
            else:
                conn.send(b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
                try:
                    with open("ESP32_acamera.html", 'r') as file:
                        html = file.read()
                except OSError:
                    html = "<h1>Archivo no encontrado"
                conn.send(html)
        except Exception as ex:
            print('Error en la conexión: ', ex)
        finally:
            conn.close() # Cerrar la conexión con el cliente

if __name__ == '__main__':
    try:
        ip = conectar_wifi(ssid, password)
        inicializar_camara()
        iniciar_servidor(ip)
    except KeyboardInterrupt:
        cam.deinit()
        print("Servidor detenido")