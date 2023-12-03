import re

VOLTAJE_RESOLUCION = 5/1023
VOLTAJE_DC = 12
VOLTAJE_AC = 140
AMPERAJE = 5
TEMPERATURA = 100
VOLTAJE_MAX = 5

def convertidor_serial(bytraje):
    if re.search("[A-Z]+[A-Z]", str(bytraje)):
        return str(bytraje)
    else:
        lectura_i = int.from_bytes(bytraje,byteorder="big")
        return float(lectura_i)*VOLTAJE_RESOLUCION


def calcular_voltaje_DC(valor):
    return valor * VOLTAJE_DC/VOLTAJE_MAX


def calcular_amperaje(valor):
    return valor * AMPERAJE/VOLTAJE_MAX


def calcular_temperatura(valor):
    return valor * TEMPERATURA


def calcular_voltaje_AC(valor):
    return valor * VOLTAJE_AC/VOLTAJE_MAX

# TEST
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
