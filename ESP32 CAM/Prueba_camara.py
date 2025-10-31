import camera
import time

err = camera.init(0, d0=11, d1=9, d2=8, d3=10, d4=12, d5=18, d6=17, d7=16, xclk=15, pclk=13, vsync=6, href=7, sioc=4, siod=5, reset=-1, pwdn=-1)
print("Resultado init:", err)

if err == 0:
    camera.framesize(camera.FRAME_QVGA)
    camera.pixformat(camera.PIXFORMAT_JPEG)
    time.sleep(1)
    img = camera.capture()
    if img:
        print("Imagen capturada, tamaño:", len(img))
        with open("test.jpg", "wb") as f:
            f.write(img)
        print("Guardada como test.jpg")
    else:
        print("No se pudo capturar imagen.")
else:
    print("Error al inicializar cámara.")

    