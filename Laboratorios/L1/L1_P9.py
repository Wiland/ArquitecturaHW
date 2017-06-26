import RPi.GPIO as GPIO
import time
 # to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
# set up the GPIO channels - one input and one output
led1 = 12
led2 = 13
led3 = 15
led4 = 19
led5 = 21
led6 = 23
in_pin1 = 11
in_pin2 = 16
GPIO.setup(in_pin1, GPIO.IN)
GPIO.setup(in_pin2, GPIO.IN)
GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
GPIO.setup(led3, GPIO.OUT)
GPIO.setup(led4, GPIO.OUT)
GPIO.setup(led5, GPIO.OUT)
GPIO.setup(led6, GPIO.OUT)

while True:
##    GPIO.setup(in1, GPIO.IN)
##    GPIO.setup(in2, GPIO.IN)
    in1 = GPIO.input(in_pin1)
    in2 = GPIO.input(in_pin2)
    
    if in1 ==1 and in2 == 1:
        print("Secuencia1")
        GPIO.output(led1, 1)
        time.sleep(0.5)
        GPIO.output(led2, 1)
        time.sleep(0.5)
        GPIO.output(led3, 1)
        time.sleep(0.5)
        GPIO.output(led4, 1)
        time.sleep(0.5)
        GPIO.output(led5, 1)
        time.sleep(0.5)
        GPIO.output(led6, 1)
        time.sleep(0.5)
    if in1 == 1 and in2 == 0:
        print("Secuencia2")
        GPIO.output(led6, 1)
        time.sleep(0.5)
        GPIO.output(led5, 1)
        time.sleep(0.5)
        GPIO.output(led4, 1)
        time.sleep(0.5)
        GPIO.output(led3, 1)
        time.sleep(0.5)
        GPIO.output(led2, 1)
        time.sleep(0.5)
        GPIO.output(led1, 1)
        time.sleep(0.5)
    elif in1 == 0 and in2 == 1:
        print("Secuencia3")
        GPIO.output(led1, 1)
        time.sleep(0.5)
        GPIO.output(led6, 1)
        time.sleep(0.5)
        GPIO.output(led2, 1)
        time.sleep(0.5)
        GPIO.output(led5, 1)
        time.sleep(0.5)
        GPIO.output(led3, 1)
        time.sleep(0.5)
        GPIO.output(led4, 1)
        time.sleep(0.5)
    elif in1 == 0 and in2 == 0:
        print("Secuencia4")
        GPIO.output(led3, 1)
        time.sleep(0.5)
        GPIO.output(led4, 1)
        time.sleep(0.5)
        GPIO.output(led2, 1)
        time.sleep(0.5)
        GPIO.output(led5, 1)
        time.sleep(0.5)
        GPIO.output(led1, 1)
        time.sleep(0.5)
        GPIO.output(led6, 1)
        time.sleep(0.5)
    GPIO.output(led1, 0)
    GPIO.output(led2, 0)
    GPIO.output(led3, 0)
    GPIO.output(led4, 0)
    GPIO.output(led5, 0)
    GPIO.output(led6, 0)
        
