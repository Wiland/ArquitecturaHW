import RPi.GPIO as GPIO
 # to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# set up the GPIO channels - one input and one output
GPIO.setup(17, GPIO.IN)
GPIO.setup(18, GPIO.OUT)
while True:
	# input from pin 17
	input_value = GPIO.input(17)
	 # output to pin 128
	GPIO.output(18,input_value)
