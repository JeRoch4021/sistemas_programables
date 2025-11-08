import cv2
import numpy as np

prototxt = "C:/Users/fabri/OneDrive/Documentos/MicroPython/deploy.prototxt" # Ruta al archivo prototxt
model = "C:/Users/fabri/OneDrive/Documentos/MicroPython/res10_300x300_ssd_iter_140000.caffemodel" # Ruta al archivo caffemodel
net = cv2.dnn.readNetFromCaffe(prototxt, model) # Cargar el modelo DNN

def iniciar_camara(ip):
    URL_CAMARA = f"http://{ip}:8080/video" # URL de la cámara IP
    cap = cv2.VideoCapture(URL_CAMARA)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 4. Preprocesamiento para DNN
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))

        # 5. Detección de rostros
        net.setInput(blob)
        detections = net.forward()

        # 6. Dibujar resultados
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            
            # Filtro de confianza (70%)
            if confidence > 0.7:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (x1, y1, x2, y2) = box.astype("int")
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                text = f"Rostro: {confidence * 100:.2f}%"
                cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Mostrar el frame
        cv2.imshow("Deteccion Facial (DNN)", frame)

        # Salir con 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    # Liberar recursos
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    ip = '192.168.1.2' # Reemplazar con la IP del servidor de la cámara
    iniciar_camara(ip)
