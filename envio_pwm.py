import RPi.GPIO as GPIO
# inicialización del puerto a usar
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)

# creación del objeto pwm
pwm = GPIO.PWM(25, 500)  # pin, frecuencia de trabajo
pwm.start(0)  # duty cicle inicial de 0, se puede poner cualquier valor

continuar = True
while continuar:
    dato = input("Digitel el nuevo Duty Cicle: ")
    if dato == "fin":
        continuar = False
    else:
        pwm.ChangeDutyCycle(int(dato))

pwm.stop()
GPIO.cleanup()
print("Fin de la carga")
