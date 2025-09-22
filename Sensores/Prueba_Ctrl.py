from machine import Pin
from ir_rx import NEC_16

def callback_ir(data, addr, ctrl):
    print("Codigo recibido: ", hex(data))
    
ir = NEC_16(Pin(15, Pin.IN), callback_ir)