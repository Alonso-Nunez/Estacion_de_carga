from envio_pwm import *

bateria_pwm = iniciar_pwm(500,100)
continuar = True
while continuar:
    dato = input("Digitel el nuevo Duty Cicle: ")
    if dato == "fin":
        continuar = False
    else:
        actualizar_dc(bateria_pwm,dato)

parar_pwm(bateria_pwm)
GPIO.cleanup()