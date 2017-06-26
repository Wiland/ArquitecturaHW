# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

"""Definición de variables"""
segments = [11,12,13,15,16,18,19]
displays = [21,22,23,24]
sw0_prt = 3
sw1_prt = 5
buzzer = 26
##buzzer = 2

global sw0 
global sw1
global hora #Contador de hora
global hora_aux #Reslpado de la hora
global contador_encendido #Contador de encendido para parpadeo del display (Cambio de alarma y reloj)
global contador_apagado #Contador de apagado para parpadeo del display (Cambio de alarma y reloj)
global display_actual #Display actual para el cambio de alarma y de hora
global contador_tiempo_pulso #Contador para pulsos antes del cambio de display (400 milisegundos)
global contador_tiempo_alarma #Tiempo que ha sonado la alarma
global contador_tiempo_alarma_encendida #Tiempo que ha sonado la alarma (Intervalo encendido-apagado)
global contador_tiempo_alarma_apagada #Tiempo que ha estado apagada la alarma (Intervalo apagado-encendido)
global contador_int_alarmas #Contador de interrupciones para cambio de alarma luego de 5 segundos sin interrupciones
global alarma_activa #Indicador de alarma activada (Global)
global alarma_activa_aux #Indicador de alarma activada (Cada intervalo encendido-apagado)
global alarmas #Vector de alarmas
global segundo #Cálculo de segundo
global minuto #Calculo de minutos
global interrupciones #Contador de interrupciones para cambio de hora en displays
global alarma_actual #Alarma que actualmente se está editando
global contador_cambio_alarma #Tiempo desde la última interrupción para cambio de alarma
global sleep_time

alarmas = [
    '9999',
    '9999',
    '9999',
    '9999',
    '9999',
    '9999',
    '9999',
    '9999',
    '9999',
    '9999',
    '9999',
    '9999',
    '9999',
    '9999',
    '9999',
    '9999',
    '9999',
    '9999',
    '9999',
    '9999'
]

interrupciones = 0
sleep_time = 0.001
segundo = 1000
minuto = 1000
contador_tiempo_alarma = contador_tiempo_alarma_encendida = contador_tiempo_alarma_apagada = 0
alarma_activa = alarma_activa_aux = 0
contador_tiempo_pulso = 0
display_actual = 0
sw0 = sw1 = 0
pulsador = 7
hora = '0000'
contador_encendido = 0
contador_apagado = 0
cuenta_tiempo = 0
alarma_actual = 0
contador_cambio_alarma = contador_int_alarmas = 0

"""Matriz alarmas"""


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
GPIO.setup(buzzer, GPIO.OUT)
GPIO.setup(sw0_prt, GPIO.IN)
GPIO.setup(sw1_prt, GPIO.IN)
GPIO.setup(pulsador, GPIO.IN)

GPIO.output(displays,1)
GPIO.output(buzzer,0)

def interruptPulsador(canal):
    global sw0
    global sw1
    global alarma_activa
    global alarma_activa_aux
    global alarma_actual
    global interrupciones
    global contador_cambio_alarma
    global contador_int_alarmas
    global hora
    global sleep_time
    
    if sw0 == 1 and sw1 == 0: #Cambio hora
        interrupciones += 1
    elif sw0 == 0 and sw1 == 1: #Alarma
        interrupciones += 1
        if contador_int_alarmas == 0:
            if alarmas[alarma_actual] == '9999':
                hora = '0000'
            else:
                hora = alarmas[alarma_actual]
                
        contador_int_alarmas += 1
    elif sw0 == 0 and sw1 == 0: #Reloj
        alarma_activa = alarma_activa_aux = 0
        contador_tiempo_alarma_encendida = contador_tiempo_alarma_apagada = 0
        contador_tiempo_alarma = 0
    
    contador_cambio_alarma = 0

def cambiarHoraDisplays(accion):
    global contador_tiempo_pulso
    global contador_encendido
    global contador_apagado
    global contador_int_alarmas
    global display_actual
    global hora
    global hora_aux
    global cuenta_tiempo
    global interrupciones
    global contador_tiempo_alarma
    global contador_cambio_alarma
    global contador_int_alarmas
    global alarma_actual
    
    if accion == 'A': #Alarma
        contador_cambio_alarma += 1
        if contador_cambio_alarma >= segundo*5:
            contador_cambio_alarma = 0
            contador_int_alarmas = 0
            alarmas[alarma_actual] = hora
            if alarma_actual < (len(alarmas)-1):
                alarma_actual += 1
            else:
                alarma_actual = 0
        if contador_int_alarmas == 0:
            hora = str(alarma_actual+1).zfill(4)
    
    for digit in range(4):
        for loop in range(0,7):
            GPIO.output(segments[loop], num[hora[digit]][loop])

        if contador_tiempo_pulso > segundo/3:
            contador_tiempo_pulso = 0
            if interrupciones == 1:
                horatxt = list(hora)

                if display_actual == 0:
                    if int(hora[display_actual+1]) > 4:
                        if int(hora[display_actual]) < 1:
                            horatxt[display_actual] = str(int(hora[display_actual]) + 1)
                        else:
                            horatxt[display_actual] = '0'
                    else:
                        if int(hora[display_actual]) < 2:
                            horatxt[display_actual] = str(int(hora[display_actual]) + 1)
                        else:
                            horatxt[display_actual] = '0'
                elif display_actual == 1:
                    if int(hora[display_actual-1]) > 1:
                        if int(hora[display_actual]) < 3:
                            horatxt[display_actual] = str(int(hora[display_actual]) + 1)
                        else:
                            horatxt[display_actual] = '0'
                    else:
                        if int(hora[display_actual]) < 9:
                            horatxt[display_actual] = str(int(hora[display_actual]) + 1)
                        else:
                            horatxt[display_actual] = '0'
                elif display_actual == 2:
                    if int(hora[display_actual]) < 5:
                        horatxt[display_actual] = str(int(hora[display_actual]) + 1)
                    else:
                        horatxt[display_actual] = '0'
                elif display_actual == 3:
                    if int(hora[display_actual]) < 9:
                        horatxt[display_actual] = str(int(hora[display_actual]) + 1)
                    else:
                        horatxt[display_actual] = '0'
                
                hora = "".join(horatxt)
                if accion == 'M':
                    hora_aux = hora
            elif interrupciones > 1:
                if display_actual < 3:
                    display_actual = (display_actual + 1)
                else:
                    display_actual = 0
            interrupciones = 0
            
        if accion == 'A':
            if contador_encendido < 500 and contador_int_alarmas != 0:
                contador_encendido += 1
                GPIO.output(displays[digit], 0) #Encender
            elif contador_int_alarmas == 0:
                GPIO.output(displays[digit], 0) #Encender
            else:
                if contador_apagado < 500:
                    contador_apagado += 1
                else:
                    contador_encendido = 0
                    contador_apagado = 0
                    
                if digit == display_actual:
                    GPIO.output(displays[digit], 1) #Apagar
                else:
                    GPIO.output(displays[digit], 0) #Encender
                    
        else:    
            if contador_encendido < 500:
                contador_encendido += 1
                GPIO.output(displays[digit], 0) #Encender
            else:
                if contador_apagado < 500:
                    contador_apagado += 1
                else:
                    contador_encendido = 0
                    contador_apagado = 0
                    
                if digit == display_actual:
                    GPIO.output(displays[digit], 1) #Apagar
                else:
                    GPIO.output(displays[digit], 0) #Encender

        time.sleep(sleep_time)
        cuenta_tiempo += 1
        contador_tiempo_pulso += 1 #contar milisegundos para pulsador
        contador_tiempo_alarma += 1
        contador_cambio_alarma += 1
        GPIO.output(displays[digit], 1)
        
def aumentarHora(cambia_hora):
    global cuenta_tiempo
    global segundo
    global minuto
    global hora
    global hora_aux
    
    if cuenta_tiempo >= minuto:
        cuenta_tiempo = 0
        if int(hora_aux[2:4]) == 59:
            if int(hora_aux[0:2]) == 23:
                hora_aux = '0000'
            else:
                hora_aux = str(int(hora_aux[0:2])+1).zfill(2)+'00'
        else:
            hora_aux = hora_aux[0:2]+str(int(hora_aux[2:4])+1).zfill(2)
    
    if cambia_hora == 1:
        hora = hora_aux

try:
    hora_aux = hora = str(time.ctime()[11:13]+time.ctime()[14:16])
    GPIO.add_event_detect(pulsador,GPIO.RISING, callback=interruptPulsador, bouncetime=200)
    while True:
        sw0 = GPIO.input(sw0_prt)
        sw1 = GPIO.input(sw1_prt)
        if sw0 == 0 and sw1 == 0: #Ver reloj
            hora = hora_aux
            alarma_actual = 0
            display_actual = 0
            aumentarHora(1)

            try:
                if alarmas.index(hora) <> None:
                    contador_tiempo_alarma = 0
                    alarma_activa = alarma_activa_aux = 1
            except ValueError:
                pass
            
            for digit in range(4):
                for loop in range(0,7):
                    GPIO.output(segments[loop], num[hora[digit]][loop])
                GPIO.output(displays[digit], 0)
                time.sleep(sleep_time)
                GPIO.output(displays[digit], 1)
                
                cuenta_tiempo += 1
                contador_tiempo_alarma += 1
                
                if alarma_activa == 1:
                    if alarma_activa_aux == 0:
                        if contador_tiempo_alarma_apagada > segundo*2:
                            contador_tiempo_alarma_encendida = 0
                            contador_tiempo_alarma_apagada = 0
                            alarma_activa_aux = 1
                        else:
                            contador_tiempo_alarma_apagada += 1
                    else:
                        if contador_tiempo_alarma_encendida >= segundo*4.5:
                            alarma_activa_aux = 0
                        else:
                            contador_tiempo_alarma_encendida += 1
                            
        elif sw0 == 1 and sw1 == 0: #Actualizar reloj
            cambiarHoraDisplays('M')
            alarma_actual = 0
        elif sw0 == 0 and sw1 == 1: #Alarmas
            aumentarHora(0)
            cambiarHoraDisplays('A')

        if contador_tiempo_alarma > (segundo*27):
            contador_tiempo_alarma_apagada = 0
            contador_tiempo_alarma_encendida = 0
            contador_tiempo_alarma = 0
            alarma_activa = 0
            alarma_activa_aux = 0
            
        GPIO.output(buzzer, alarma_activa_aux)
finally:
    GPIO.cleanup()
