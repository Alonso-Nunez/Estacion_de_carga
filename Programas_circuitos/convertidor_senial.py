import re
import math

VOLTAJE_RESOLUCION = 5/1023
VOLTAJE_DC = 12
VOLTAJE_AC = 140
RESOLUCION_VOLTAJE_AC = 127/14
AMPERAJE = 5
TEMPERATURA = 100
VOLTAJE_MAX = 5
RAIZ_DOS = math.sqrt(2)


def convertidor_serial(bytraje):
    """
    Función que convierte los bytes recibidos de la comunicación serial en un entero o un mensaje

    Args:
        bytraje (bytes): Bytes recibidos de la comunición serial

    Returns:
        str: Mensaje obtenido en caso de no ser números
        float: valor obtenido de la comunicación serial 
    """
    if re.search("[A-Z]+[A-Z]", str(bytraje)):
        return str(bytraje)
    else:
        lectura_i = int.from_bytes(bytraje, byteorder="big")
        return float(lectura_i)*VOLTAJE_RESOLUCION


def calcular_voltaje_DC(valor):
    """Función que retorna el valor real del voltaje a 12v DC

    Args:
        valor (float): valor obtenido de la función de converidor_serial()

    Returns:
        float: valor real de la medición
    """
    return valor * VOLTAJE_DC/VOLTAJE_MAX


def calcular_amperaje(valor):
    """Función que retorna el valor real del amperaje a 5v DC

    Args:
        valor (float): valor obtenido de la función de converidor_serial()

    Returns:
        float: valor real de la medición
    """
    return valor * AMPERAJE/VOLTAJE_MAX


def calcular_temperatura(valor):
    """Función que retorna el valor real de la temperatura a 5v DC

    Args:
        valor (float): valor obtenido de la función de converidor_serial()

    Returns:
        float: valor real de la medición
    """
    return valor * TEMPERATURA


def calcular_voltaje_AC(valor):
    """Función que retorna el valor real del voltaje a 140v AC

    Args:
        valor (float): valor obtenido de la función de converidor_serial()

    Returns:
        float: valor real de la medición
    """
    return ((valor*4)/RAIZ_DOS) * RESOLUCION_VOLTAJE_AC


# TEST
'''
try:
    while True:
        data = b'\xff'#bytes(input("Escribe la cadena de bytes\n"),'utf-8')
        valor = convertidor_serial(data)
        print(valor)
        if type(valor) == type("cadena"):
            print (valor)
        else:
            sel = int(input("Selecciona la opción a ocupar:\n1->VDC\n2->VAC\n3->Amp\n4->Temp\n"))
            if sel == 1:
                print(calcular_voltaje_DC(valor))
            elif sel == 2:
                print(calcular_voltaje_AC(valor))
            elif sel == 3:
                print(calcular_amperaje(valor))
            elif sel == 4:
                print(calcular_temperatura(valor))
            else:
                print("Opción no valida")
except:
    print("ERROR")
'''
