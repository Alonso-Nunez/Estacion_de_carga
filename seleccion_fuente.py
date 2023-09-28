import time
import RPi.GPIO as GPIO


def peso_ponderado(fuente,valor):
    """
    Función pondera el valor de las mediciones de las entradas.

    Args:
        fuente (int): fuente seleccionada a ponderar
        1   Panel solar
        2   Aerogenerador
        3   Bateria
        4   Suministro CFE
        valor (float): valor obtenido de la medicion de los voltajes

    Returns:
        float: valor ponderado del voltaje obtenido mediante mediciones
    """
    if fuente== 0:
        if float(valor)*8.3<83:
            return 0
        return float(valor)*8.3
    elif fuente == 1:
        if float(valor)*6.9<69:
            return 0
        return float(valor)*6.9
    elif fuente == 2:
        if float(valor)*5.7<57:
            return 0
        return float(valor)*5.7
    else :
        return float(valor)*0.4
      

def pasa_panel(instruccion):
    """
    Función que enciende o apaga la fuente (Panel solar) según sea necesario

    Args:
        instruccion (int): instrucción de apagar/prender (0/1)
    """
    #GPIO.setmode(GPIO.BCM)
    #GPIO.setup(23, GPIO.OUT)
    if instruccion == 0:
        GPIO.output(23, GPIO.LOW)
    elif instruccion == 1:
        GPIO.output(23, GPIO.HIGH)
    else:
        print("Instruccion no encontrada")
    #GPIO.cleanup()

    
def pasa_aero(instruccion):
    """
    Función que enciende o apaga la fuente (Aerogenerador) según sea necesario

    Args:
        instruccion (int): instrucción de apagar/prender (0/1)
    """
    #GPIO.setmode(GPIO.BCM)
    #GPIO.setup(24, GPIO.OUT)
    if instruccion == 0:
        GPIO.output(24, GPIO.LOW)
    elif instruccion == 1:
        GPIO.output(24, GPIO.HIGH)
    else:
        print("Instruccion no encontrada")
    #GPIO.cleanup()
  

def pasa_cfe(instruccion):
    """
    Función que enciende o apaga la fuente (Cfe) según sea necesario

    Args:
        instruccion (int): instrucción de apagar/prender (0/1)
    """
    #GPIO.setmode(GPIO.BCM)
    #GPIO.setup(22, GPIO.OUT)
    if instruccion == 0:
        GPIO.output(22, GPIO.LOW)
    elif instruccion == 1:
        GPIO.output(22, GPIO.HIGH)
    else:
        print("Instruccion no encontrada")
    #GPIO.cleanup()
     
   
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
    ponderadoCfe =  peso_ponderado(3, voltajeCfe)
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