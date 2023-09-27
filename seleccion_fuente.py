import time
import threading as th
import RPi.GPIO as GPIO

def pesoPonderado(fuente,valor):
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
    

def pasaPanel(instruccion):
    """
    Función que enciende o apaga la fuente (Panel solar) según sea necesario

    Args:
        instruccion (int): instrucción de apagar/prender (0/1)
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(9, GPIO.OUT)
    if instruccion == 0:
        GPIO.output(9, GPIO.LOW)
    elif instruccion == 1:
        GPIO.output(9, GPIO.HIGH)
    else:
        print("Instruccion no encontrada")
        
def pasaAero(instruccion):
    """
    Función que enciende o apaga la fuente (Aerogenerador) según sea necesario

    Args:
        instruccion (int): instrucción de apagar/prender (0/1)
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(10, GPIO.OUT)
    if instruccion == 0:
        GPIO.output(10, GPIO.LOW)
    elif instruccion == 1:
        GPIO.output(10, GPIO.HIGH)
    else:
        print("Instruccion no encontrada")
        
def pasaCfe(instruccion):
    """
    Función que enciende o apaga la fuente (Cfe) según sea necesario

    Args:
        instruccion (int): instrucción de apagar/prender (0/1)
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(11, GPIO.OUT)
    if instruccion == 0:
        GPIO.output(11, GPIO.LOW)
    elif instruccion == 1:
        GPIO.output(11, GPIO.HIGH)
    else:
        print("Instruccion no encontrada")
        
    
GPIO.setmode(GPIO.BCM)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
Panel = {"nombre":"PanelSolar","puerto":9,"estado":False, "valor":0}
Aero = {"nombre":"Aerogenerador","puerto":10, "estado":False,"valor":1}
Cfe = {"nombre":"CFE","puerto":11,"estado":False, "valor":3}
try:
    voltajePanel = input("Ingresa el voltaje del Panel Solar: ")
    voltajeAero = input("Ingresa el voltaje del Aerogenerador: ")
    voltajeCfe = input("Ingresa el voltaje de CFE: ")

    ponderadoPanel = pesoPonderado(Panel.get("valor"), voltajePanel)
    ponderadoAero = pesoPonderado(Aero.get("valor"), voltajeAero)
    ponderadoCfe =  pesoPonderado(Cfe.get("valor"), voltajeCfe)
    
    arreglo=[ponderadoCfe,ponderadoAero,ponderadoPanel]
    arreglo.sort(reverse=True)
    print(arreglo)
    
    if arreglo[0] == ponderadoPanel:
        pasaPanel(1)
    elif arreglo[0] == ponderadoAero:
        pasaAero(1)
    elif arreglo[0] == ponderadoCfe:
        pasaCfe(1)
    else :
        pasaCfe(0)
        pasaAero(0)
        pasaPanel(0)
    time.sleep(10)
    
except:
    print("error")
    
finally:
    GPIO.cleanup()
    pasaCfe(0)
    pasaAero(0)
    pasaPanel(0)







        
