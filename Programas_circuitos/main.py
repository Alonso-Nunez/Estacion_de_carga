import time
import threading as thr
from envio_pwm import *
from seleccion_fuente import *
from conexion_mongo import *
from conexion_serial import *
from estado_carga import *
from convertidor_senial import *
from switches import *
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
GPIO.setup(12, GPIO.IN)

# Constante
MENSAJE_PIC = ["V1", "V2", "V3",
               "V4", "V5", "I1",  "I2", "TM"]
BATERIA_CARGADA = 12
TEMPERATURA_MAX = 45
lecturaPIC = ["", "", "", "", "", "", "", ""]

# Conexiones externas
conSerial = crear_conexion_serial()


def intercambio_datos_PIC(mensaje):
    """
    Función que consulta los valores de las mediciones e ingresan ese valor
    a la cadena lectruaPIC
    Args:
        mensaje (String): Instruccion a enviar al PIC

    Returns:
        bool: Envio de mensaje Exitoso o no
    """
    if envio_valores(conSerial, mensaje):
        if mensaje.index == 0:
            lecturaPIC[mensaje.index] = str(calcular_voltaje_DC(
                convertidor_serial(leer_valores(conSerial))))
        elif mensaje.index == 1:
            lecturaPIC[mensaje.index] = str(calcular_voltaje_DC(
                convertidor_serial(leer_valores(conSerial))))
        elif mensaje.index == 2:
            lecturaPIC[mensaje.index] = str(calcular_voltaje_DC(
                convertidor_serial(leer_valores(conSerial))))
        elif mensaje.index == 3:
            lecturaPIC[mensaje.index] = str(calcular_voltaje_AC(
                convertidor_serial(leer_valores(conSerial))))
        elif mensaje.index == 4:
            lecturaPIC[mensaje.index] = str(calcular_voltaje_DC(
                convertidor_serial(leer_valores(conSerial))))
        elif mensaje.index == 5:
            lecturaPIC[mensaje.index] = str(calcular_amperaje(
                convertidor_serial(leer_valores(conSerial))))
        elif mensaje.index == 6:
            lecturaPIC[mensaje.index] = str(calcular_amperaje(
                convertidor_serial(leer_valores(conSerial))))
        elif mensaje.index == 7:
            lecturaPIC[mensaje.index] = str(calcular_temperatura(
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


def paso_fuentes():
    """
    Función que seleciona la fuente que suministra corriente al circuito de carga
    Se hace lectura cada minuto
    """
    alimentacion = True
    while alimentacion:
        arregloFuentes = acomodo_ponderado(
            peso_ponderado(0, lecturaPIC[0]),
            peso_ponderado(1, lecturaPIC[1]),
            peso_ponderado(2, lecturaPIC[2]),
            peso_ponderado(3, lecturaPIC[3]))
        fuente = activar_fuente(arregloFuentes,
                                lecturaPIC[0],
                                lecturaPIC[1],
                                lecturaPIC[2],
                                lecturaPIC[3])
        time.sleep(50)


def obtener_datos():
    envioDB = True
    while envioDB:
        for mensaje in MENSAJE_PIC:
            while intercambio_datos_PIC(mensaje) == False:
                intercambio_datos_PIC(mensaje)
        guardar_datos_db()
        time.sleep(60)


def estado_cargas():
    """Función que asigna el estado de las cargas del auto y bateria
    """
    global cargarAuto
    global cargarBateria
    cargarAuto = cargaAuto()
    cargarBateria = not cargarAuto
    time.sleep(10)


def principal():
    try:
        hiloCargas = thr.Thread(target=estado_cargas)
        hiloCargas.setDaemon(True)
        hiloCargas.start()
        # Variables globales para control de hilos
        global continuarEntradas
        global alimentacion
        global envioDB
        global fuente
        inicio_serial = True
        # Inicio de programa controlado por una buena cominucación serial
        while inicio_serial:
            envio_valores(conSerial, "HI")
            if convertidor_serial(leer_valores(conSerial)) == "OK":
                inicio_serial = False
        # Inicio de Hilo para guardar los datos leidos en la base de datos
        hiloEnvioDatosBD = thr.Thread(target=obtener_datos)
        hiloEnvioDatosBD.setDaemon(True)
        hiloEnvioDatosBD.start()
        io_bateria(0)
        io_inversor(0)
        io_carga(0)
        global power
        power = iniciar_pwm(1000, 0)

        while True:
            if cargarAuto == True and cargarBateria == False:
                io_carga(0)
                io_bateria(0)
                alimentacion = False
                time.sleep(60)
                hiloPasoFuente = thr.Thread(target=paso_fuentes)
                hiloPasoFuente.setDaemon(True)
                hiloPasoFuente.start()
                actualizar_dc(power, 0)
                if fuente < 2:  # Se carga con aerogenerador o panel solar
                    io_inversor(1)
                elif fuente == 2:  # Se carga con bateria
                    actualizar_dc(power, 100)
                    io_inversor(1)
                    io_bateria(1)
                elif fuente == 3:  # Se carga con energia de CFE
                    actualizar_dc(power, 100)
                    io_inversor(0)
                    io_bateria(0)
            elif cargarBateria == True and cargarAuto == False:
                io_bateria(0)
                io_inversor(0)
                alimentacion = False
                time.sleep(60)
                hiloPasoFuente = thr.Thread(target=paso_fuentes)
                hiloPasoFuente.setDaemon(True)
                hiloPasoFuente.start()
                if fuente > 2:  # Solo se carga con panel solar o aerogenerado
                    actualizar_dc(power, 0)
                    if float(lecturaPIC[2]) >= BATERIA_CARGADA:
                        io_carga(0)
                        cargarBateria = False
                    else:
                        io_inversor(0)
                        io_bateria(0)
                        io_carga(1)

            elif cargarBateria == False and cargarAuto == False:
                alimentacion = False
                time.sleep(60)
                actualizar_dc(power, 100)
                io_bateria(0)
                io_inversor(0)
                io_carga(0)

    except Exception as error:
        print(error)

    finally:
        cerrar_conexion_serial(conSerial)
        apagar_fuentes()
        cargarAuto = False
        cargarBateria = False
        alimentacion = False
        envioDB = False
        time.sleep(65)
        GPIO.cleanup()


hiloPrincipal = thr.Thread(target=principal)
io_bateria(0)
io_inversor(0)
io_carga(0)
hiloPrincipal.start()
