import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

segments = [11,12,13,15,16,18,19]
displays = [21,22,23,24]
sw0_prt = 3
sw1_prt = 5

sw0 = sw1 = 0

pulsador = 7
contador = 0000
GPIO.setup(displays, GPIO.OUT)
GPIO.setup(segments, GPIO.OUT)
GPIO.setup(sw0_prt, GPIO.IN)
GPIO.setup(sw1_prt, GPIO.IN)

num = {' ':(1,1,1,1,1,1,1),
    '0':(0,0,0,0,0,0,1),
    '1':(1,0,0,1,1,1,1),
    '2':(0,0,1,0,0,1,0),
    '3':(0,0,0,0,1,1,0),
    '4':(1,0,0,1,1,0,0),
    '5':(0,1,0,0,1,0,0),
    '6':(0,1,0,0,0,0,0),
    '7':(0,0,0,1,1,1,1),
    '8':(0,0,0,0,0,0,0),
    '9':(0,0,0,0,1,0,0)}

GPIO.output(displays,0)

def interruptPulsador(canal):
    global sw1
    global sw2
    if sw0 == 0 and sw1 == 0:
        print("Secuencia1")
        global contador
        contador = 0000
    elif sw0 == 1 and sw1 == 0:
        print("Secuencia2")
        contador = 0000
    elif sw0 == 0 and sw1 == 1:
        print("Secuencia3")
        contador = 0000
    print("Interrupcion")
    
try:
    while True:
        sw0 = GPIO.input(sw0_prt)
        sw1 = GPIO.input(sw1_prt)
        print('SW0-'+str(sw0)+'.......SW1-'+str(sw1))
        if sw0 == 0 and sw1 == 0: #Ver reloj
            print("Secuencia1")
            n = str(time.ctime()[11:13]+time.ctime()[14:16])
            for digit in range(4):
                for loop in range(0,7):
                    GPIO.output(segments[loop], num[n[digit]][loop])
                GPIO.output(displays[digit], 0)
                time.sleep(0.0001)
                GPIO.output(displays[digit], 1)
        elif sw0 == 1 and sw1 == 0: #Actualizar reloj
            print("Secuencia2")
        elif sw0 == 0 and sw1 == 1: #Alarmas
            print("Secuencia3")
finally:
    GPIO.output(segments, 1)
