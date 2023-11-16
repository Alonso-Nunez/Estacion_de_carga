from seleccion_fuente import *
import time
import RPi.GPIO as GPIO

# Iniciaclización de los puertos GPIO a usar
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)


try:
    voltajePanel = input("Ingresa el voltaje del Panel Solar: ")
    voltajeAero = input("Ingresa el voltaje del Aerogenerador: ")
    voltajeCfe = input("Ingresa el voltaje de CFE: ")
    #Ponderación de los valores obtenidos
    ponderadoPanel = peso_ponderado(0, voltajePanel)
    ponderadoAero = peso_ponderado(1, voltajeAero)
    ponderadoCfe =  peso_ponderado(2, voltajeCfe)
    #Creacion de un arreglo que se acomoda
    arreglo=[ponderadoCfe,ponderadoAero,ponderadoPanel]
    arreglo.sort(reverse=True)
    print(arreglo)
    #Selector
    if arreglo[0] == ponderadoPanel:
        pasa_panel(1)
    elif arreglo[0] == ponderadoAero:
        pasa_aero(1)
    elif arreglo[0] == ponderadoCfe:
        pasa_cfe(1)
    else :
        pasa_cfe(0)
        pasa_aero(0)
        pasa_panel(0)
    time.sleep(10)  

except:
    print("error")
finally:
    pasa_cfe(0)
    pasa_aero(0)
    pasa_panel(0)
    GPIO.cleanup()