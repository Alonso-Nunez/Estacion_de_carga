import time
import threading as thr
from envio_pwm import *
from seleccion_fuente import *
from switches import *
from conexion_mongo import *
from conexion_serial import *
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
            if cargarBateria == False:
                io_bateria(1)
        else:
            io_bateria(0)
        time.sleep(60)


def principal():
    try:
        # Variables globales para control de hilos
        global continuarEntradas
        global cargar
        global cargarBateria
        global alimentacion
        global envioDB

        while True:
            cargar = True # Cambiar cuando sea posible
            cargarBateria = not cargar
            envioDB = cargar and cargarBateria

            if cargar:
                io_inversor(1)
                while cargar:
                    for mensaje in MENSAJE_PIC:
                        while intercambio_datos_PIC(mensaje)==False:
                            intercambio_datos_PIC(mensaje)
                    guardar_datos_db()
                    hiloPasoFuente = thr.Thread(target=paso_fuentes)
                    hiloPasoFuente.start()
            elif cargarBateria:
                io_inversor(0)
                io_bateria(1)
                while cargarBateria and cargar == False:
                    for mensaje in MENSAJE_PIC:
                        while intercambio_datos_PIC(mensaje)==False:
                            intercambio_datos_PIC(mensaje)
                    guardar_datos_db()
                    hiloPasoFuente = thr.Thread(target=paso_fuentes)
                    hiloPasoFuente.start()
                    pwmBateria = iniciar_pwm(1000,100)
                    if float(lecturaPIC[2]) >= 12:
                        parar_pwm(pwmBateria)
                        cargarBateria = False
                    io_bateria(1)
            elif cargarBateria == False and cargar == False:
                envioDB = True
                io_bateria(0)
                io_inversor(0)

                while envioDB:
                    for mensaje in MENSAJE_PIC:
                        while intercambio_datos_PIC(mensaje)==False:
                            intercambio_datos_PIC(mensaje)
                    guardar_datos_db()
                    envioDB = cargar and cargarBateria

    except Exception as error:
        print (error)
    finally:
        cerrar_conexion_serial(conSerial)
        continuarEntradas = apagar_fuentes()
        cargar = False
        cargarBateria = False
        alimentacion = False
        parar_pwm(pwmBateria)
        envioDB = False

hiloPrincipal = thr.Thread(target=principal)
io_bateria(0)
io_inversor(0)
hiloPrincipal.start()

