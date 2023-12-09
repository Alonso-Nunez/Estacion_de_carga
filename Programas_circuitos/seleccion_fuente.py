import RPi.GPIO as GPIO
import switches as sw
# import time


# Iniciaclización de los puertos GPIO a usar
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)


def peso_ponderado(fuente, valor):
    """
    Función pondera el valor de las mediciones de las entradas.

    Args:
        fuente (int): fuente seleccionada a ponderar
        0   Panel solar
        1   Aerogenerador
        2   Bateria
        3   Suministro CFE
        valor (float): valor obtenido de la medicion de los voltajes

    Returns:
        float: valor ponderado del voltaje obtenido mediante mediciones
    """
    if fuente == 0:
        if float(valor)*8.3 < 83:
            return 0
        return float(valor)*8.3
    elif fuente == 1:
        if float(valor)*6.9 < 69:
            return 0
        return float(valor)*6.9
    elif fuente == 2:
        if float(valor)*5.7 < 57:
            return 0
        return float(valor)*5.7
    else:
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
    arreglo = [float(ponderadoPanel), float(ponderadoAero),
               float(ponderadoBateria), float(ponderadoCFE)]
    print("no ordenado", arreglo)
    arreglo.sort(reverse=True)
    return arreglo


def activar_fuente(arreglo, pP, pA, pB, pC):
    """
    Funcion que activa el paso de corriente de la fuente seleccionada

    Args:
        arreglo (array): arreglo con los valores de los pesos ponderados ordenados
        pP (float): Valor ponderado de la lectura del Panel Solar
        pA (float): Valor ponderado de la lectura del Aerogenerador
        pB (float): Valor ponderado de la lectura de la Bateria
        pC (float): Valor ponderado de la lectura de CFE
    """
    print(arreglo, pP, pA, pB, pC)
    if arreglo[0] == float(pP):
        pasa_aero(0)
        pasa_cfe(0)
        pasa_panel(1)
        return 0
    elif arreglo[0] == float(pA):
        pasa_panel(0)
        pasa_aero(0)
        pasa_aero(1)
        return 1
    elif arreglo[0] == float(pB):
        pasa_aero(0)
        pasa_panel(0)
        pasa_cfe(0)
        return 2
    elif arreglo[0] == float(pC):
        pasa_panel(0)
        pasa_aero(0)
        pasa_cfe(1)
        return 3
    else:
        pasa_cfe(0)
        pasa_aero(0)
        pasa_panel(0)
        sw.io_bateria(0)
        return 10


def apagar_fuentes():
    """
    Función que apaga todas las fuentes

    Returns:
        bool: Retorna falso para que las fuentes no se activen hasya nuevo aviso
    """
    pasa_cfe(0)
    pasa_aero(0)
    pasa_panel(0)
    sw.io_bateria(0)


'''
try:
    voltajePanel = input("Ingresa el voltaje del Panel Solar: ")
    voltajeAero = input("Ingresa el voltaje del Aerogenerador: ")
    voltajeCfe = input("Ingresa el voltaje de CFE: ")
    # Ponderación de los valores obtenidos
    ponderadoPanel = peso_ponderado(0, voltajePanel)
    ponderadoAero = peso_ponderado(1, voltajeAero)
    ponderadoCfe = peso_ponderado(3, voltajeCfe)
    # Creacion de un arreglo que se acomoda
    arreglo = acomodo_ponderado(ponderadoPanel, ponderadoAero, 0, ponderadoCfe)
    print(arreglo)
    # Selector
    activar_fuente(arreglo, ponderadoPanel, ponderadoAero, ponderadoCfe)
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
    # pasa_panel(1)
    # pasa_aero(1)
    # pasa_cfe(1)
    print("encendido")
    time.sleep(10)
    print("Apagado")
    # pasa_panel(0)
    # pasa_aero(0)
    # 12pasa_cfe(0)

except:
    print("error")
finally:
    pasa_cfe(0)
    pasa_aero(0)
    pasa_panel(0)
    GPIO.cleanup()
'''
