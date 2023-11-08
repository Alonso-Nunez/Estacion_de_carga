import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(11, GPIO.IN)

def cargaAuto():
    """
    Función que verifica si esta pulsado el boton de carga de vehiculo

    Returns:
        Boolean: True en caso de que se pida cargar el vehiculo
    """
    if(GPIO.input(11) == 1):
        return True
    return False