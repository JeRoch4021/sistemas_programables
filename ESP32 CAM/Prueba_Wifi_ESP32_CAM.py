import network
import time

def conectar_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.disconnect()  # Limpia estado anterior
    wlan.connect(ssid, password)
    print("Conectando a WiFi...")
    
    for _ in range(20):
        if wlan.isconnected():
            print("Conectado!")
            print("IP:", wlan.ifconfig()[0])
            return True
        time.sleep(0.5)
        print(".", end="")
    print("\nError: No se pudo conectar.")
    return False

# Cambia por tu red
conectar_wifi("rochasainez", "35631354")