import camera

camera.deinit()  # Limpia el estado anterior
camera.init(0, format=camera.JPEG)
camera.framesize(camera.FRAME_QVGA)

img = camera.capture()
if img:
    with open("foto.jpg", "wb") as f:
        f.write(img)
    print("Foto guardada como foto.jpg")
else:
    print("No se pudo capturar imagen")

camera.deinit()

    