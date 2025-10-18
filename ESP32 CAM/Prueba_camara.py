import camera

try:
    camera.init()
    camera.framesize(1)
    
    print("Cámara inicializada correctamente.")
    
    buf = camera.capture()
    
    # 3. VERIFICACIÓN: Comprueba si buf es False antes de usar len()
    if buf:
        # La captura fue exitosa
        print("Captura de imagen realizada.")
        print("Tamaño del buffer:", len(buf))
        # Aquí es donde guardarías o enviarías 'buf'
    else:
        # La captura falló (buf es False)
        print("Error: La captura de imagen falló (camera.capture() devolvió False).")
        print("Posible problema: PSRAM insuficiente o fallo de lectura del sensor.")
    
except Exception as e:
    print("Error al inicializar la cámara:", e)