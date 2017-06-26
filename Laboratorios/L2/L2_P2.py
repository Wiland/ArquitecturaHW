import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

segments = [11,12,13,15,16,18,19]
displays = [21,22,23,24]

pulsador = 7
pulsos = 0
GPIO.setup(displays, GPIO.OUT)
GPIO.setup(pulsador, GPIO.IN)
GPIO.setup(segments, GPIO.OUT)

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
    global pulsos
    pulsos += 1

try:
    GPIO.add_event_detect(pulsador,GPIO.RISING,callback=interruptGPIO, bouncetime=200)
    while True:
        n = str(pulsos).rjust(4)
        for digit in range(4):
            for loop in range(0,7):
                GPIO.output(segments[loop], num[n[digit]][loop])
            GPIO.output(displays[digit], 0)
            time.sleep(0.001)
            GPIO.output(displays[digit], 1)
finally:
    GPIO.cleanup()
