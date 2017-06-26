from RPLCD import CharLCD
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23])

sw0_prt = 11
sw1_prt = 12
sw2_prt = 13
buzzer = 15
pul = 7
sw0 = 0
sw1 = 0
sw2 = 0
contadorpulsos = 0 # variable aux de pulsos
contadorpulsos2 = 0 # variable aux de pulsos en el juego 
tiempopulsador1 = 0 # variable aux de tiempo en pulsos
tiempojugador = 0 # Variable para el punto 3
tiempojuego = 0 # variable de tiempo de juego
resultadojuego = 0 # Resultado del tiempo jugado
tiempo = 0 # tiempo sonoro
segundo = 1000 # segundo sonoro por milisegundos
contador = 0 # contador de iteraciones
gana = 0 # ganan el juego
sonidobuzzer = 0 # sonido del buzzer
archivo = 0 # Variable que almacena el archivo
contenidoArchivo = 0 # Variable que almacena el contenido del archivo


#Configurar funciones iniciales

GPIO.setup(sw0_prt, GPIO.IN)
GPIO.setup(sw1_prt, GPIO.IN)
GPIO.setup(sw2_prt, GPIO.IN)
GPIO.setup(pul, GPIO.IN)
GPIO.setup(buzzer, GPIO.OUT)

def tiempoEntreInterrupcion(cosas):
    global sw0
    global sw1
    global sw2
    global pul
    global contadorpulsos
    global contadorpulsos2
    global tiempopulsador1
    global tiempojuego
    global resultadojuego
    global buzzer
    global tiempo
    global gana
    global sonidobuzzer
    
    if sw0 == 0 and sw1 == 0 and sw2 == 1:
        contadorpulsos += 1
        if contadorpulsos == 1:
            tiempopulsador1 = int(round(time.time() * 1000))
        elif contadorpulsos == 2:
            tiempojuego = int(round(time.time() * 1000)) - tiempopulsador1
            lcd.cursor_pos = (0, 0)
            lcd.write_string("Ya puede empezar")
            lcd.cursor_pos = (1, 0)
            lcd.write_string("a jugar!")
            print(tiempojuego)
        elif contadorpulsos == 3:
            lcd.clear()
            lcd.write_string("Solo dos")
            lcd.cursor_pos = (1, 0)
            lcd.write_string("pulsaciones")

    if sw0 == 0 and sw1 == 1 and sw2 == 0:
        lcd.clear()
        lcd.write_string("Jugando")
        contadorpulsos2 += 1
        if contadorpulsos2 == 1:
            tiempo  = 0
            gana = 0
            tiempopulsador1 = int(round(time.time() * 1000))
            print(tiempopulsador1)
        elif contadorpulsos2 == 2:
            tiempojugador = int(round(time.time() * 1000)) - tiempopulsador1
            lcd.cursor_pos = (0, 0)
            resultadojuego = 100 - abs(tiempojugador - tiempojuego)/100
            print(resultadojuego)
            if resultadojuego > 95:
                lcd.clear()
                lcd.write_string("Ganaste!")
                tiempo = 0
                sonidobuzzer = 1
                gana = 1
            else:
                lcd.write_string("No ganaste :(")
            contadorpulsos2 = tiempojugador = 0
try:
    aux = 0
    GPIO.output(buzzer, 0)
    GPIO.add_event_detect(pul, GPIO.RISING, callback=tiempoEntreInterrupcion, bouncetime=200)
    while True:
        sw0 = GPIO.input(sw0_prt)
        sw1 = GPIO.input(sw1_prt)
        sw2 = GPIO.input(sw2_prt)
        
        if sw0 == 0 and sw1 == 0 and sw2 == 0:
            aux = 1
            lcd.cursor_pos = (0, 0)
            lcd.write_string("Hora: %s" %time.strftime("%H:%M:%S"))
            lcd.cursor_pos = (1, 0)
            lcd.write_string("Fech: %s" %time.strftime("%d/%m/%Y"))
            if contadorpulsos != 0 or contadorpulsos2 != 0:
                lcd.clear()
            contadorpulsos = contadorpulsos2 = tiempojugador = gana = resultadojuego = 0
            time.sleep(0.001)
            
        elif sw0 == 0 and sw1 == 0 and sw2 == 1:
            if contadorpulsos == 0:
                lcd.clear()
            time.sleep(0.001)
            
        elif sw0 == 0 and sw1 == 1 and sw2 == 0:
            aux = 0
            if gana == 0:
                if tiempo >= 10:
                    lcd.clear()
                    lcd.cursor_pos = (1, 0)
                    lcd.write_string("Presionar nuevamente")
                    contadorpulsos2 = 0
            else:
                if tiempo >= 5:
                    sonidobuzzer = 0

            GPIO.output(buzzer, sonidobuzzer)
            time.sleep(0.001)
            contador += 1
        elif sw0 == 0 and sw1 == 1 and sw2 == 1:
            if contadorpulsos != 0 or contadorpulsos2 != 0 or aux == 1:
                lcd.clear()
            aux = 0
            hot = "hot"
            apariciones = 0
            with open("archivolectura.txt","r") as f:
                apariciones = f.read().lower().count(hot)
            lcd.cursor_pos = (0, 0)
            lcd.write_string("'HOT' aparece %s veces" %apariciones)
        elif sw0 == 1 and sw1 == 0 and sw2 == 0:
            contadorpulsos = contadorpulsos2 = tiempojugador = gana = resultadojuego = 0
            
        if contador == segundo:
            tiempo += 1
            print(tiempo)
            contador = 0
finally:
    lcd.clear()
    GPIO.cleanup()




   

    
