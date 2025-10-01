from machine import Pin
from time import sleep

# Motor Derecho
in1 = machine.Pin(17, Pin.OUT)
in2 = machine.Pin(27, Pin.OUT) 
en_a = machine.Pin(4, Pin.OUT)

# Motor Izquierdo
in3 = machine.Pin(5, Pin.OUT) 
in4 = machine.Pin(6, Pin.OUT) 
en_b = machine.Pin(13, Pin.OUT) 
q=PWM(en_a,freq =100, duty=512)
p=PWM(en_b,freq =100, duty=512)
p.start(75)
q.start(75)

#Se inicializan apagados los motores
in1.off()
in2.off()
in3.off()
in4.off()

try:
    # Ciclo infinito de lectura
    while(True):
        # Lee la entrada de teclado y la 
        muestra
        user_input = input()
        print(user_input)
        if user_input == 'w':
            in1.on()
            in2.off()
            in3.off()
            in4.on()
            print("Adelante") 
        elif user_input == 's':
            in1.off()
            in2.on()
            in3.on()
            in4.off()
            print('Atrás')
        elif user_input == 'd':
            in1.off()
            in2.on()
            in3.off()
            in4.off()
            print('Derecha')
        elif user_input == 'a':
            in1.on()
            in2.off()
            in3.off()
            in4.off()
            print('Izquierda')
        # Detener 
        elif user_input == 'e':
            in1.off()
            in2.off()
            in3.off()
            in4.off()
            print('Stop')  
