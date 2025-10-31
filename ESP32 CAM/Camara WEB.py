import network
import camera
import socket
import time

# ------------------------------
# 1️⃣ Conectar a la Wi-Fi
# ------------------------------

SSID = "Megacable_2.4G_D0CB"      # Cambia esto
PASSWORD = "43hxGnD5"    # Cambia esto

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Conectando a Wi-Fi...")
timeout = 15  # segundos
while not wlan.isconnected() and timeout > 0:
    time.sleep(1)
    timeout -= 1
    print(".", end="")
print()

if wlan.isconnected():
    ip = wlan.ifconfig()[0]
    print("¡Wi-Fi conectada! IP:", ip)
else:
    print("No se pudo conectar a la Wi-Fi")
    raise SystemExit

# ------------------------------
# 2️⃣ Inicializar la cámara
# ------------------------------
try:
    camera.init()
    camera.framesize(8)  # 240x240
    print("Cámara lista")
except Exception as e:
    print("Error al iniciar la cámara:", e)
    raise SystemExit

# ------------------------------
# 3️⃣ Servidor web para fotos
# ------------------------------
addr = (ip, 80)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(addr)
s.listen(1)
print("Servidor web activo en http://%s" % ip)

while True:
    cl, addr = s.accept()
    print("Conexión desde:", addr)
    request = cl.recv(1024)
    
    if b"GET /foto" in request:
        try:
            img = camera.capture()
            cl.send(b"HTTP/1.0 200 OK\r\nContent-Type: image/jpeg\r\n\r\n")
            cl.send(img)
        except Exception as e:
            cl.send(b"HTTP/1.0 500 Internal Server Error\r\n\r\n")
            cl.send(b"<h1>Error al capturar foto</h1>")
    else:
        cl.send(b"HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n")
        cl.send(b"<h1>ESP32-S3-CAM</h1>")
        cl.send(b'<p>Ir a <a href="/foto">/foto</a> para ver la foto</p>')
    
    cl.close()
