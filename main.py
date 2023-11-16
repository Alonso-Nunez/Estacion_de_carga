import time
import threading as thr
from envio_pwm import *
from seleccion_fuente import *
from switches import *
from conexion_mongo import *
from conexion_serial import *
from estado_carga import *
#import RPi.GPIO as GPIO
'''
GPIO.setmode(GPIO.BCM)
# Uso switches
GPIO.setup(5,GPIO.OUT)
GPIO.setup(6,GPIO.OUT)
# Uso selector de fuente
GPIO.setup(22, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
# Uso PWM
GPIO.setup(25, GPIO.OUT)
'''
# Constante
MENSAJE_PIC = ["vol_Panel", "vol_Aero", "vol_Bat", "vol_CFE","vol_Inv", "int_Ent",  "int_Inv", "tem_Bat"]
BATERIA_CARGADA = 13
lecturaPIC = ["", "", "", "", "", "", "", ""]

# Conexiones externas
conSerial = crear_conexion_serial()

def intercambio_datos_PIC(mensaje):
    """
    Función que consulta los valores de las me
    Args:
        mensaje (String): Instruccion a enviar al PIC

    Returns:
        bool: Envio de mensaje Exitoso o no
    """
    if envio_valores(mensaje):
        lecturaPIC[mensaje.index] = str(leer_valores(conSerial))
        return True
    else:
        print ("Error en el envio de datos lectura")
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
        if activar_fuente(arregloFuentes,
                        lecturaPIC[0],
                        lecturaPIC[1],
                        lecturaPIC[3]) == 0:
            if cargarAuto:
                io_bateria(1)
        else:
            io_bateria(0)
        time.sleep(60)

def estado_cargas():
    """Función que asigna el estado de las cargas del auto y bateria
    """
    global cargarAuto
    global cargarBateria
    global envioDB
    cargarAuto = cargaAuto()
    cargarBateria = not cargarAuto # Reemplazar con función de ¿Cargar bateria?
    envioDB = cargarAuto and cargarBateria
    time.sleep(10)

def principal():
    try:
        hiloCargas = thr.Thread(target=estado_cargas)
        hiloCargas.setDaemon()
        hiloCargas.start()
        # Variables globales para control de hilos
        global continuarEntradas
        global alimentacion

        while True:

            if cargarAuto:
                io_inversor(1)
                alimentacion = False
                time.sleep(60)
                hiloPasoFuente = thr.Thread(target=paso_fuentes)
                hiloPasoFuente.setDaemon()
                hiloPasoFuente.start()
                io_bateria(0)
                while cargarAuto:
                    for mensaje in MENSAJE_PIC:
                        while intercambio_datos_PIC(mensaje)==False:
                            intercambio_datos_PIC(mensaje)
                    guardar_datos_db()

            elif cargarBateria:
                io_inversor(0)
                io_bateria(1)
                alimentacion = False
                time.sleep(60)
                hiloPasoFuente = thr.Thread(target=paso_fuentes)
                hiloPasoFuente.setDaemon()
                hiloPasoFuente.start()
                while cargarBateria and cargarAuto == False:
                    for mensaje in MENSAJE_PIC:
                        while intercambio_datos_PIC(mensaje)==False:
                            intercambio_datos_PIC(mensaje)
                    guardar_datos_db()
                    pwmBateria = iniciar_pwm(1000,100)
                    if float(lecturaPIC[2]) >= BATERIA_CARGADA:
                        parar_pwm(pwmBateria)
                        cargarBateria = False
                    io_bateria(1)

            elif cargarBateria == False and cargarAuto == False:
                envioDB = True
                io_bateria(0)
                io_inversor(0)
                alimentacion = False
                while envioDB:
                    for mensaje in MENSAJE_PIC:
                        while intercambio_datos_PIC(mensaje)==False:
                            intercambio_datos_PIC(mensaje)
                    guardar_datos_db()
                    envioDB = cargarAuto and cargarBateria

    except Exception as error:
        print (error)
        
    finally:
        cerrar_conexion_serial(conSerial)
        continuarEntradas = apagar_fuentes()
        cargarAuto = False
        cargarBateria = False
        alimentacion = False
        parar_pwm(pwmBateria)
        envioDB = False

hiloPrincipal = thr.Thread(target=principal)
io_bateria(0)
io_inversor(0)
hiloPrincipal.start()

