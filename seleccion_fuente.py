import time
import RPi.GPIO as GPIO


# Iniciaclización de los puertos GPIO a usar
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)


def peso_ponderado(fuente,valor):
    """
    Función pondera el valor de las mediciones de las entradas.

    Args:
        fuente (int): fuente seleccionada a ponderar
        0   Panel solar
        1   Aerogenerador
        x   Bateria
        2   Suministro CFE
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
    if instruccion == 0:
        GPIO.output(23, GPIO.LOW)
    elif instruccion == 1:
        GPIO.output(23, GPIO.HIGH)
    else:
        print("Instruccion no encontrada")

    
def pasa_aero(instruccion):
    """
    Función que enciende o apaga la fuente (Aerogenerador) según sea necesario

    Args:
        instruccion (int): instrucción de apagar/prender (0/1)
    """
    if instruccion == 0:
        GPIO.output(24, GPIO.LOW)
    elif instruccion == 1:
        GPIO.output(24, GPIO.HIGH)
    else:
        print("Instruccion no encontrada")
  

def pasa_cfe(instruccion):
    """
    Función que enciende o apaga la fuente (Cfe) según sea necesario

    Args:
        instruccion (int): instrucción de apagar/prender (0/1)
    """
    if instruccion == 0:
        GPIO.output(22, GPIO.LOW)
    elif instruccion == 1:
        GPIO.output(22, GPIO.HIGH)
    else:
        print("Instruccion no encontrada")

def acomodo_ponderado(ponderadoPanel, ponderadoAero, ponderadoBateria, ponderadoCFE):
    """
    Funcion que crea un arreglo con los pesos ponderados acomododados de mayor a menor

    Args:
        ponderadoPanel (float): Valor ponderado de la lectura del Panel Solar
        ponderadoAero (float): Valor ponderado de la lectura del Aerogenerador
        ponderadoBateria (float): Valor ponderado de la bateria
        ponderadoCFE (float): Valor ponderado de CFE

    Returns:
        arreglor array: arreglo ordenado con los valores de mayor a menor
    """
    arreglo = [float(ponderadoPanel), float(ponderadoAero), float(ponderadoBateria), float(ponderadoCFE)]
    arreglo.sort(reverse=True)
    return arreglo

def activar_fuente(arreglo,pP ,pA ,pC):
    """
    Funcion que activa el paso de corriente de la fuente seleccionada

    Args:
        arreglo (array): arreglo con los valores de los pesos ponderados ordenados
        pP (float): Valor ponderado de la lectura del Panel Solar
        pA (float): Valor ponderado de la lectura del Aerogenerador
        pC (float): Valor ponderado de la lectura de CFE
    """
    if arreglo[0] == float(pP):
        pasa_panel(1)
    elif arreglo[0] == float(pA):
        pasa_aero(1)
    elif arreglo[0] == float(pC):
        pasa_cfe(1)
    else :
        pasa_cfe(0)
        pasa_aero(0)
        pasa_panel(0)

def apagar_fuentes():
    """
    Función que apaga todas las fuentes

    Returns:
        bool: Retorna falso para que las fuentes no se activen hasya nuevo aviso
    """
    pasa_cfe(0)
    pasa_aero(0)
    pasa_panel(0)
    return False