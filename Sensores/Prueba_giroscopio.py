# Importar las bibliotecas necesarias
import machine
import time
from mpu6050 import MPU6050
# Configurar el bus I2C
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))
# Inicializar el MPU6050
mpu = MPU6050(i2c)

# Mostrar los valores del acelerómetro y el giroscopio en la consola
while True:
    # Leer los valores del acelerómetro y el giroscopio
    values = mpu.get_values()
    ax = values['AcX']
    ay = values['AcY']
    az = values['AcZ']
    gx = values['GyX']
    gy = values['GyY']
    gz = values['GyZ']
    
    # Mostrar los valores del acelerómetro y el giroscopio en la consola
    print('Acelerometro:')
    print('Ax={0:.2f}g'.format(ax))
    print('Ay={0:.2f}g'.format(ay))
    print('Az={0:.2f}g'.format(az))
    print('Giroscopio:')
    print('Gx={0:.2f}dps'.format(gx))
    print('Gy={0:.2f}dps'.format(gy))
    print('Gz={0:.2f}dps'.format(gz))
    # Esperar un segundo antes de volver a leer los valores del MPU6050
    time.sleep(1)