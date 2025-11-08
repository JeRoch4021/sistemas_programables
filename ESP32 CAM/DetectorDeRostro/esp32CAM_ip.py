import camera
import network
import socket
import time

def conectar_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        time.sleep(1)
        print('.', end='')
    #print('\n¡Conexión exitosa!')
    #print('Dirección IP asignada:', wlan.ifconfig()[0])
    return wlan.ifconfig()[0]

def iniciar_camara():
    camera.init()
    camera.framesize(8)  # 320x240, estable y rápido

def iniciar_servidor(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 🔹 permite reutilizar el puerto
    s.bind(('0.0.0.0', 8080))
    s.listen(1)
    print(f"Servidor de streaming en: http://{ip}:8080/video")
    return s

def stream(conn):
    conn.send('HTTP/1.1 200 OK\r\nContent-Type: multipart/x-mixed-replace; boundary=frame\r\n\r\n')
    while True:
        try:
            img = camera.capture()
            conn.send(b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + img + b'\r\n')
        except Exception as e:
            #print("Cliente desconectado o error:", e)
            break

def main():
    ssid = 'Megacable_2.4G_D0CB'
    password = '43hxGnD5'
    ip = conectar_wifi(ssid, password)
    iniciar_camara()
    s = iniciar_servidor(ip)

    while True:
        conn, addr = s.accept()
        #print('Cliente conectado desde', addr)
        stream(conn)
        conn.close()

if __name__ == '__main__':
    main()