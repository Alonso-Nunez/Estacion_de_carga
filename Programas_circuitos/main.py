import time
import threading as thr
from seleccion_fuente import *
from conexion_mongo import *
from conexion_serial import *
from estado_carga import *
from convertidor_senial import *
from switches import *
from envio_pwm import *
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
# Uso switches
GPIO.setup(5, GPIO.OUT)  # switch bateria
GPIO.setup(6, GPIO.OUT)  # switch inversor
GPIO.setup(13, GPIO.OUT)  # switch cargar bateria
# Uso selector de fuente
GPIO.setup(22, GPIO.OUT)  # switch CFE
GPIO.setup(23, GPIO.OUT)  # switch Panel
GPIO.setup(24, GPIO.OUT)  # switch Aero
# Uso PWM
GPIO.setup(25, GPIO.OUT)
# Uso de activador
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Constante
MENSAJE_PIC = ["V1", "V2", "V3", "V4", "V5", "A1",  "A2", "TM"]
BATERIA_CARGADA = 12
TEMPERATURA_MAX = 45
lecturaPIC = ["", "", "", "", "", "", "", ""]


def intercambio_datos_PIC(mensaje, posicion):
    """
    Función que consulta los valores de las mediciones e ingresan se valor
    a la cadena lectruaPIC
    Args:
        mensaje (String): Instruccion a enviar al PIC

    Returns:
        bool: Envio de mensaje Exitoso o no
    """
    if envio_valores(conSerial, mensaje):
        # print("Mensaje enviado: ", mensaje, posicion)
        if posicion == 0:
            lecturaPIC[0] = str(calcular_voltaje_DC(
                convertidor_serial(leer_valores(conSerial))))
        elif posicion == 1:
            lecturaPIC[1] = str(calcular_voltaje_DC(
                convertidor_serial(leer_valores(conSerial))))
        elif posicion == 2:
            lecturaPIC[2] = str(calcular_bateria(
                convertidor_serial(leer_valores(conSerial))))
        elif posicion == 3:
            lecturaPIC[3] = str(calcular_voltaje_AC(
                convertidor_serial(leer_valores(conSerial))))
        elif posicion == 4:
            lecturaPIC[4] = str(calcular_bateria(
                convertidor_serial(leer_valores(conSerial))))
        elif posicion == 5:
            lecturaPIC[5] = str(calcular_amperaje(
                convertidor_serial(leer_valores(conSerial))))
        elif posicion == 6:
            lecturaPIC[6] = str(calcular_amperaje(
                convertidor_serial(leer_valores(conSerial))))
        elif posicion == 7:
            lecturaPIC[7] = str(calcular_temperatura(
                convertidor_serial(leer_valores(conSerial))))
        else:
            print(convertidor_serial(leer_valores(conSerial)))
        return True
    else:
        print("Error en el envio de datos lectura")
        return False


def guardar_datos_db():
    """Función que envia los datos leidos a la base de datos
    """
    insertar_datos(lecturaPIC)
    print("Datos guardados ", lecturaPIC)


def paso_fuentes():
    """
    Función que seleciona la fuente que suministra corriente al circuito de carga
    Se hace lectura cada minuto
    """
    # print("Entrando Paso de fuentes")
    pP = peso_ponderado(0, lecturaPIC[0])
    pA = peso_ponderado(1, lecturaPIC[1])
    pB = peso_ponderado(2, lecturaPIC[2])
    pC = peso_ponderado(3, lecturaPIC[3])
    arregloFuentes = acomodo_ponderado(pP, pA, pB, pC)
    fuente = activar_fuente(arregloFuentes, pP, pA, pB, pC)
    print("Fuente seleccionada : ", fuente)
    return fuente


def obtener_datos():
    envioDB = True
    while envioDB:
        for mensaje in MENSAJE_PIC:
            # print("Antes de intercambio", mensaje, MENSAJE_PIC.index(mensaje))
            while intercambio_datos_PIC(mensaje, MENSAJE_PIC.index(mensaje)) == False:
                print("Error al enviar ", mensaje)
                time.sleep(0.5)
        guardar_datos_db()
        time.sleep(5)


'''
def estado_cargas():
    """Función que asigna el estado de las cargas del auto y bateria
    """
    global cargarAuto
    global cargarBateria
    cargarAuto = cargaAuto()
    cargarBateria = not cargarAuto
    time.sleep(10)
'''

try:
    # Apagado de todos los switches
    io_bateria(0)
    io_inversor(0)
    io_carga(0)
    # Conexiones externas
    conSerial = crear_conexion_serial()
    # Inicio de programa controlado por una buena cominucación serial
    inicio_serial = True
    while inicio_serial:
        envio_valores(conSerial, "HI")
        recibido = convertidor_serial(leer_valores(conSerial))
        print("Envio de HI")
        time.sleep(1)
        if recibido == str(b'OK'):
            inicio_serial = False
            print("Iniciando programa principal")
        else:
            print(recibido)
    # Variables globales para control de hilos
    global alimentacion
    global envioDB
    global power
    # Inicio de Hilo para guardar los datos leidos en la base de datos
    hiloEnvioDatosBD = thr.Thread(target=obtener_datos)
    hiloEnvioDatosBD.setDaemon(True)
    hiloEnvioDatosBD.start()
    # No se permite el paso de corriente en el módulo de potencia
    power = iniciar_pwm(1000, 100)
    time.sleep(0.5)

    while True:
        cargarAuto, cargarBateria = carga(lecturaPIC[2])
        print("Estados", cargarAuto, cargarBateria)
        if cargarAuto and not cargarBateria:
            print("Cargar Auto?")
            # Apagado del switch de carga de la bateria
            io_carga(0)
            fuente = paso_fuentes()
            # lógica del cargador
            if fuente < 2:  # Se carga con aerogenerador o panel solar
                print("Se selecciono la fuente: ", fuente)
                io_bateria(0)
                # Se permite el paso de corriente en el módulo de potencia
                actualizar_dc(power, 0)
                io_inversor(1)
            elif fuente == 2:  # Se carga con bateria
                if float(lecturaPIC[7]) < TEMPERATURA_MAX:
                    print("Se selecciono la bateria")
                    # No se permite el paso de corriente en el módulo de potencia
                    actualizar_dc(power, 100)
                    io_inversor(1)
                    io_bateria(1)
            elif fuente == 3:  # Se carga con energia de CFE
                print("Se selecciono CFE: ")
                # No se permite el paso de corriente en el módulo de potencia
                actualizar_dc(power, 100)
                io_inversor(0)
                io_bateria(0)
        elif cargarBateria and not cargarAuto:
            print("Cargar Bateria?")
            # Apagado de switches del inversor y descarga de bateria
            io_bateria(0)
            io_inversor(0)
            fuente = paso_fuentes()
            # Lógica de la carga de la bateria
            # Solo se carga con panel solar o aerogenerador
            if fuente < 2 and float(lecturaPIC[7]) < TEMPERATURA_MAX:
                if float(lecturaPIC[2]) >= BATERIA_CARGADA:
                    print("Bateria cargada")
                    # No se permite el paso de corriente en el módulo de potencia
                    actualizar_dc(power, 100)
                    io_carga(0)
                    cargarBateria = False
                else:
                    print("Iniciando carga de bateria")
                    io_inversor(0)
                    io_bateria(0)
                    io_carga(1)
                    # Se permite el paso de corriente en el módulo de potencia
                    actualizar_dc(power, 0)
        elif not cargarBateria and not cargarAuto:
            # No hay elementos que requieran carga
            print("Rutina de descanso")
            # NO se permite le paso de corriente en el módilo de potencia
            actualizar_dc(power, 100)
            # Se apagan todos los switches
            io_bateria(0)
            io_inversor(0)
            io_carga(0)
        time.sleep(1)

except Exception as error:
    print(error)

finally:
    print("Fin de programa")
    cerrar_conexion_serial(conSerial)
    apagar_fuentes()
    cargarAuto = False
    cargarBateria = False
    envioDB = False
    GPIO.cleanup()
    # parar_pwm(power)
    time.sleep(32)
