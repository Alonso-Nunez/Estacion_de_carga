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
# Constantes
MONGO_BD = "Prueba_cargador"
MONGO_COLECCION = "Bateria" 
MENSAJE_PIC = ["vol_Panel", "vol_Aero", "vol_Bat", "vol_CFE","vol_Inv", "int_Ent",  "int_Inv", "tem_Bat"]
lecturaPIC = ["", "", "", "", "", "", "", ""]

# Conexiones externas
conDB, coleccion, base = conectar_db(MONGO_BD,MONGO_COLECCION)
conSerial = crear_conexion_serial()

def intercambio_datos_PIC(mensaje):
    if envio_valores(mensaje):
        lecturaPIC[mensaje.index] = str(leer_valores(conSerial))
        return True
    else:
        print ("Error en el envio de datos lectura")
        return False

def guardar_datos_db():
    insertar_datos(conDB)
    time.sleep(1)

def paso_fuentes():
    while continuarEntradas:
        arregloFuentes = acomodo_ponderado(
                peso_ponderado(0, lecturaPIC[0]),
                peso_ponderado(1, lecturaPIC[1]),
                peso_ponderado(2, lecturaPIC[2]),
                peso_ponderado(3, lecturaPIC[3]))
        activar_fuente(arregloFuentes,lecturaPIC[0],lecturaPIC[1],lecturaPIC[3])
        time.sleep(600)


def principal():
    try:
        global continuarEntradas
        cargar = True
        while cargar:
            for mensaje in MENSAJE_PIC:
                while intercambio_datos_PIC(mensaje)==False:
                    intercambio_datos_PIC(mensaje)
            continuarEntradas= True
            hiloDB = thr.Thread(target=guardar_datos_db)
            hiloDB.start()
            hiloPasoFuente = thr.Thread(target=paso_fuentes)
            hiloPasoFuente.start()
            
            


    except RuntimeError as error:
        print (error)
    finally:
        desconectar_db(conDB)
        cerrar_conexion_serial(conSerial)
        continuarEntradas = apagar_fuentes()

hiloPrincipal = thr.Thread(target=principal)
hiloPrincipal.start()

