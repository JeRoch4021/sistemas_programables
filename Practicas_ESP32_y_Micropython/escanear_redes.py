import network
import time

def scan_networks():
    #Escanea las redes Wi-Fi disponibles y muestra información detallada de cada
    #una. Retorna una lista de SSIDs de las redes encontradas
    wlan = network.WLAN(network.STA_IF)
    
    wlan.active(True)
    print("Escaneadno redes Wi-Fi..")
    networks = wlan.scan()
    available_networks = []
    
    authmodes = {
    0: 'Open',
    1: 'WEP',
    2: 'WPA-PSK',
    3: 'WPA2-PSK',
    4: 'WPA/WPA2-PSK',
    5: 'WPA2-EAP',
    6: 'WPA3-PSK',
    7: 'WPA2/WPA3-PSK'
    }
    
    for idx, net in enumerate(networks):
        try:
            ssid = net[0].decode('utf-8')
        except UnicodeDecodeError:
            ssid = "<SSID no legible>"
        bssid = ':'.join(['%02x' % b for b in net[1]])  # Dirección MAC del punto de acceso
        channel = net[2] # Canal en el que opera la red             
        RSSI = net[3]    # Intensidad de la señal en dBm               
        authmode = net[4]   # Modo de autenticación de la red
        auth_str = authmodes.get(authmode, f"Desconocido ({authmode})")
        print(f"{idx + 1}: SSID: {ssid}, BSSID: {bssid}, Canal: {channel}, Señal: {RSSI} dBm, Seguridad: {auth_str}")
        available_networks.append(ssid)  # Agrega el SSID a la lista de redes disponibles
    return available_networks

def do_connect():
    #""" Escanea las redes Wi-Fi disponibles, permite al usuario seleccionar una,
    #solicita la contraseña e intenta establecer la conexión.
    wlan = network.WLAN(network.STA_IF)  # Crea una instancia de la interfaz Wi-Fi en modo estación
    wlan.active(True)                    
    available_networks = scan_networks() 
    # Activa la interfaz Wi-Fi
    # Obtiene la lista de redes disponibles
    if not available_networks:
        print("No se encontraron redes Wi-Fi disponibles.")
        return
    try:
        choice = int(input("Seleccione el número de la red a la que desea conectarse: ")) - 1
        if choice < 0 or choice >= len(available_networks):
            print("Selección no válida.")
            return
    except ValueError:
        print("Entrada no válida. Por favor, ingrese un número.")
        return
    
    ssid = available_networks[choice]    # Obtiene el SSID de la red seleccionada
    password = input(f"Ingrese la contraseña para {ssid}: ") # Solicita la contraseña al usuario
    print(f"Conectando a la red {ssid}...")
    wlan.connect(ssid, password)         
    # Intenta conectarse a la red seleccionada
    timeout = 10  # Tiempo de espera máximo en segundos para establecer la conexión
    for _ in range(timeout):
        if wlan.isconnected():
            print('Conexión establecida.')
            print('Configuración de red (IP/netmask/gw/DNS):', wlan.ifconfig())
            return
        time.sleep(1)  
    # Espera 1 segundo antes de verificar nuevamente
    print("No se pudo establecer la conexión. Verifique la contraseña e intente nuevamente.")
    
do_connect()