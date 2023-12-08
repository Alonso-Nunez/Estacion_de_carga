import RPi.GPIO as GPIO


# inicialización del puerto GPIO a usar
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)


def iniciar_pwm(f_trabajo, dc_inicial):
    """_summary_

    Args:
        f_trabajo (int): frecuencia de trabajo del pwm
        dc_inicial (int): DutyCycle inicial 

    Returns:
        pwm object: variable de tipo objeto con la información del pwm creado
    """
    pwm = GPIO.PWM(25, f_trabajo)
    pwm.start(dc_inicial)
    print("Inicio del pwm con Duty Cycle inicial de: ", dc_inicial)
    return pwm


def parar_pwm(pwm):
    """
    Detiene el pwm y lanza alerta

    Args:
        pwm (objet): objeto pwm a detener
    """
    pwm.stop()
    print("Fin de la carga")


def actualizar_dc(pwm, dc_nuevo):
    """
    Actualiza el DutyCyle del pwm seleccionado

    Args:
        pwm (object): Objeto pwm a actualizar
        dc_nuevo (int): DutyCycle a actualizar
    """
    pwm.ChangeDutyCycle(int(dc_nuevo))
    print("Ducty Cycle actualizado")

'''
bateria_pwm = iniciar_pwm(500, 100)
continuar = True
while continuar:
    dato = input("Digitel el nuevo Duty Cicle: ")
    if dato == "fin":
        continuar = False
    else:
        actualizar_dc(bateria_pwm, dato)

parar_pwm(bateria_pwm)
GPIO.cleanup()
'''
