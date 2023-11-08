import RPi.GPIO as GPIO

# Inicialización  de los puertos GPIO a usar
GPIO.setmode(GPIO.BCM)
GPIO.setup(5,GPIO.OUT)
GPIO.setup(6,GPIO.OUT)


def io_inversor(instruccion):
    """
    Función que enciende o apaga el switch del inversor

    Args:
        instruccion (int): recibe un 1 para encender o un 0 para apagar
    """
    if instruccion == 0:
        GPIO.output(6,GPIO.LOW)
    elif instruccion == 1:
        GPIO.output(6,GPIO.HIGH)
    else:
        print("Instrucción no encontrada")


def io_bateria(instruccion):
    """
    Función que enciende o apaga el switch de la bateria

    Args:
        instruccion (int): recibe un 1 para encerder o un 0 para apagar
    """
    if instruccion == 0:
        GPIO.output(5,GPIO.LOW)
    elif instruccion == 1:
        GPIO.output(5,GPIO.HIGH)
    else:
        print("Instrucción no encontrada")
