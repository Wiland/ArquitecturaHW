import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

segments = [11,12,13,15,16,18,19]

GPIO.setup(21, GPIO.OUT)
GPIO.setup(segments, GPIO.OUT)

digits = ['0','1','2','3','4','5','6','7','8','9']
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

GPIO.output(21,0)
try:
    while True:
        for digit in digits:
            for loop in range(0,7):
                GPIO.output(segments[loop], num[digit][loop])
            time.sleep(1)
finally:
    GPIO.cleanup()
