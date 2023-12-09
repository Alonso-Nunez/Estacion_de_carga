import RPi.GPIO as GPIO
# import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def carga(voltaje_bateria):
    """
    Función que verifica si esta pulsado el boton de carga de vehiculo

    Returns:
        Boolean: True en caso de que se pida cargar el vehiculo
    """
    if (GPIO.input(12) == GPIO.HIGH):
        if voltaje_bateria < 12:
            return False, True
        else:
            return False, False
        return True, False
    else:
        return False, False


'''
while True:
    auto = cargaAuto()
    print(auto)
    time.sleep(5)
'''
