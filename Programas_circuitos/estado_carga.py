import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.IN)

def cargaAuto():
    """
    Función que verifica si esta pulsado el boton de carga de vehiculo

    Returns:
        Boolean: True en caso de que se pida cargar el vehiculo
    """
    if(GPIO.input(12) == GPIO.HIGH):
        return True
    return False


while True:
    auto = cargaAuto()
    time.sleep(5)
