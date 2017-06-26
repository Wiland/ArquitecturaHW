import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

segments = [11,12,13,15,16,18,19]
displays = [21,22,23,24]
pulsador = 7
contador = 0
tiempo = 0.001
cuenta_tiempo = 0
GPIO.setup(displays, GPIO.OUT)
GPIO.setup(segments, GPIO.OUT)
GPIO.setup(pulsador, GPIO.IN)
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

def interruptGPIO(canal):
    global contador
    contador = 0000

try:
    GPIO.add_event_detect(pulsador,GPIO.RISING,callback=interruptGPIO, bouncetime=200)
    contador = int(time.ctime()[11:13]+time.ctime()[14:16])
    while True:
        if cuenta_tiempo == 1000:
            cuenta_tiempo = 0
            contador += 1
        print(str(contador)[2:4])
        if str(contador)[2:4] == str(60):
            contador[1:2] += 1
        n = str(contador).zfill(4)
        for digit in range(4):
            for loop in range(0,7):
                GPIO.output(segments[loop], num[n[digit]][loop])
            GPIO.output(displays[digit], 0)
            time.sleep(0.001)
            cuenta_tiempo += 1
            GPIO.output(displays[digit], 1)
finally:
    GPIO.output(segments, 1)
