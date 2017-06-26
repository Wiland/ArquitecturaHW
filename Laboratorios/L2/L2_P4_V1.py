# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

"""Definición de variables"""
segments = [11,12,13,15,16,18,19]
displays = [21,22,23,24]
display_actual = 0
sw0_prt = 3
sw1_prt = 5
sw0 = sw1 = 0
pulsador = 7
hora = 0000
contador_encendido = 0
contador_apagado = 0

"""Matriz de números (0-9)"""
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

##Configurar funciones iniciales de puertos
GPIO.setup(displays, GPIO.OUT)
GPIO.setup(segments, GPIO.OUT)
GPIO.setup(sw0_prt, GPIO.IN)
GPIO.setup(sw1_prt, GPIO.IN)

GPIO.output(displays,0)

def interruptPulsador(canal):
    global sw1
    global sw2
    if sw0 == 1 and sw1 == 0:
        event = GPIO.wait_for_edge(pulsador, GPIO.RISING, timeout=300)
            if event is None:
                global hora
		global display_actual
		if display_actual == 0:
                    if hora[display_actual+1] > 4:
                        if hora[display_actual] < 1:
                            hora[display_actual] = hora[display_actual] + 1
			else:
                            hora[display_actual] = 0
			else:
                            if hora[display_actual] < 2:
                                hora[display_actual] = hora[display_actual] + 1
			    else:
				hora[display_actual] = 0
		elif display_actual == 1:
                    if hora[display_actual-1] > 1:
			if hora[display_actual] < 4:
                            hora[display_actual] = hora[display_actual] + 1
			else:
                            hora[display_actual] = 0
			else:
                            if hora[display_actual] < 9:
                                hora[display_actual] = hora[display_actual] + 1
			    else:
                                hora[display_actual] = 0
		elif display_actual == 2:
                    if hora[display_actual] < 5:
			hora[display_actual] = hora[display_actual] + 1
                    else:
                        hora[display_actual] = 0
		elif display_actual == 3:
                    if hora[display_actual] < 9:
                        hora[display_actual] = hora[display_actual] + 1
		    else:
                        hora[display_actual] = 0
            else:
                global display_actual
                    if display_actual < 3:
                        display_actual = (display_actual + 1)
		    else:
                        display_actual = 0
    elif sw0 == 0 and sw1 == 1:
        print("Secuencia3")
        contador = 0000
    print("Interrupcion")
    
try:
    GPIO.add_event_detect(pulsador,GPIO.RISING,callback=interruptPulsador, bouncetime=200)
    while True:
        sw0 = GPIO.input(sw0_prt)
        sw1 = GPIO.input(sw1_prt)
        if sw0 == 0 and sw1 == 0: #Ver reloj
            print("Secuencia1")
	    global hora
            hora = str(time.ctime()[11:13]+time.ctime()[14:16])
            for digit in range(4):
                for loop in range(0,7):
                    GPIO.output(segments[loop], num[hora[digit]][loop])
                GPIO.output(displays[digit], 0)
                time.sleep(0.001)

                if contador_encendido < 500:
                    contador_encendido = contador_encendido + 1
                    GPIO.output(displays[digit], 1)
		else:
                    if digit = display_actual:
                        GPIO.output(displays[digit], 0)
                        if contador_encendido < 500:
                            contador_encendido = contador_encendido + 1
                        else:
                            contador_encendido = 0
                            contador_apagado = 0
		    else:
                        GPIO.output(displays[digit], 1)			
        elif sw0 == 1 and sw1 == 0: #Actualizar reloj
            print("Secuencia2")
            global hora
	    for digit in range(4):
                for loop in range(0,7):
                    GPIO.output(segments[loop], num[hora[digit]][loop])
                GPIO.output(displays[digit], 0)
                time.sleep(0.001)
                GPIO.output(displays[digit], 1)
        elif sw0 == 0 and sw1 == 1: #Alarmas
            print("Secuencia3")
finally:
    GPIO.output(segments, 1)
