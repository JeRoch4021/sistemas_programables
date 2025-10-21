import camera
import time

camera.init()
camera.framesize(8)
camera.pixformat(10)
time.sleep(1)

print("Tomando foto...")
img = camera.capture()

if img:
    print("¡ÉXITO! La foto se pudo tomar.")
    print("Tamaño de la imagen: " + len(img) + "bytes.")
    with open("test.jpg", "wb") as f:
        f.write(img)
    print("Foto tomada correctamente.")
else:
    print("No se pudo capturar imagen.")
    