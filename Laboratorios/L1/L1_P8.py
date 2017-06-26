import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False)
led = 18
GPIO.setup(led, GPIO.OUT) 
print ("Blinking")
for x in range(0, 9):
	GPIO.output(led, 1)
	time.sleep(1)
	GPIO.output(led, 0)
	time.sleep(1)

GPIO.cleanup()
