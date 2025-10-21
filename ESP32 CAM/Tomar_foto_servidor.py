import camera
import network
import socket

camera.init(0, format=camera.JPEG)

def tomar_foto():
    print('Tomar foto')
    camera.framesize(camera.FRAME_240X240)
    foto = camera.capture()
    f = open('imagen.jpg', 'w')
    f.write(foto)
    f.close()
    
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)