import RPi.GPIO as GPIO
 # to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# set up the GPIO channels - one input and one output
GPIO.setup(11, GPIO.IN)
GPIO.setup(12, GPIO.OUT)
while True:
	# input from pin 11
	input_value = GPIO.input(11)
	 # output to pin 12
	GPIO.output(12,input_value )
