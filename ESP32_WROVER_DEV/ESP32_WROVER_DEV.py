# Implementación de librerias
import network # Para conectarse a Wi-Fi
import socket # Para crear un servidor web
import time # Para manejar pausas
from acamera import Camera, FrameSize, PixelFormat # Para controlar el módulo de cámara OV5640

# Configuración del objeto cámara par tomar fotos y grabar videos 
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

# Función para inicializar camara
def inicializar_camara():
    try:
        cam.init() # Método de inicialización de la cámara
        time.sleep(1)
        print("Camara inicializada correctamente.")
    except Exception as ex:
        print('Error al inicializar la cámara:', ex)                

# Función para capturar una foto con la cámara y enviarla por una conexión HTTP
def enviar_foto(conn):
    try:
        frame = cam.capture()
        # Dicha foto sera guardada en una archivo ".jpg" y se alamcena en la memoria
        # del ESP32-WROVER-DEV
        with open('imagen.jpg', 'wb') as abrir_imagen:
            abrir_imagen.write(frame)
        # Usar conectores de red activa y enviar los datos que resultaron de la variable frame
        conn.send(b'HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\n\r\n')
        conn.send(frame)
    except Exception as ex:
        print("Error al capturar imagen: ", ex)
        conn.send(b"HTTP/1.1 500 Internal Server Error\r\n\r\n")

# Función para enviar streaming
def enviar_stream(conn):
    try:
        # Conector de red activa que le indica al navegador que recibira muchas imagenes
        # como si fuera un video
        conn.send(b'HTTP/1.1 200 OK\r\nContent-Type: multipart/x-mixed-replace; boundary=frame\r\n\r\n')
        while True:
            # Usamos la instrucción de captura
            frame = cam.capture()
            # Envio del frame
            conn.send(b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.1)
    except Exception as ex:
        print("Streaming detenido: ", ex)


def iniciar_servidor(ip):
    addr = (ip, 80) # Dirección IP y puerto del servidor (puerto 80 es estándar para HTTP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Crear un socket TCP/IP
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Reutiliza la dirección
    s.bind(addr) # Enlazar el socket a la dirección IP y puerto
    s.listen(5) # Escuchar conexiones entrantes
    print('Servidor web iniciado en http://%s:80' % ip)
    
    while True:
        conn, addr = s.accept() # Aceptar una conexión entrante
        print('Conexión desde:', addr)
        try:
            request = conn.recv(1024).decode() # Recibir la solicitud del cliente
            print('Solicitud recibida:', request)
            
            # Solicitud HTTP para enviar fotos
            if "GET /foto" in request:
                enviar_foto(conn)
            # Solicitud HTTP para iniciar video en vivo
            elif "GET /stream" in request:
                enviar_stream(conn)
            else:
                # Enviar página HTML por defecto
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
            
# Función para ejecutar las principales funciones del programa final
if __name__ == '__main__':
    try:
        ip = conectar_wifi(ssid, password)
        inicializar_camara()
        iniciar_servidor(ip)
    except KeyboardInterrupt:
        cam.deinit()
        print("Servidor detenido")