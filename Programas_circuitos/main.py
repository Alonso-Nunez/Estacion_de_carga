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
GPIO.setup(12, GPIO.IN)

# Constante
MENSAJE_PIC = ["V1", "V2", "V3", "V4", "V5", "I1",  "I2", "TM"]
BATERIA_CARGADA = 12
TEMPERATURA_MAX = 45
lecturaPIC = ["", "", "", "", "", "", "", ""]


def intercambio_datos_PIC(mensaje, posicion):
    """
    Función que consulta los valores de las mediciones e ingresan ese valor
    a la cadena lectruaPIC
    Args:
        mensaje (String): Instruccion a enviar al PIC

    Returns:
        bool: Envio de mensaje Exitoso o no
    """
    if envio_valores(conSerial, mensaje):
        print("Mensaje enviado: ",mensaje)
        if posicion == 0:
            lecturaPIC[0] = str(calcular_voltaje_DC(
                convertidor_serial(leer_valores(conSerial))))
        elif posicion == 1:
            lecturaPIC[1] = str(calcular_voltaje_DC(
                convertidor_serial(leer_valores(conSerial))))
        elif posicion == 2:
            lecturaPIC[2] = str(calcular_voltaje_DC(
                convertidor_serial(leer_valores(conSerial))))
        elif posicion == 3:
            lecturaPIC[3] = str(calcular_voltaje_AC(
                convertidor_serial(leer_valores(conSerial))))
        elif posicion == 4:
            lecturaPIC[4] = str(calcular_voltaje_DC(
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
    global fuente
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
            while intercambio_datos_PIC(mensaje, MENSAJE_PIC.index(mensaje)) == False:
                print("Error al enviar ", mensaje)
        guardar_datos_db()
        time.sleep(60)


def estado_cargas():
    """Función que asigna el estado de las cargas del auto y bateria
    """
    global cargarAuto
    global cargarBateria
    cargarAuto = cargaAuto()
    cargarBateria = not cargarAuto
    print(cargaAuto, cargarBateria)
    time.sleep(10)


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
        if convertidor_serial(leer_valores(conSerial)) == "OK":
            inicio_serial = False
            print("Iniciando programa principal")
            
    hiloCargas = thr.Thread(target=estado_cargas)
    hiloCargas.setDaemon(True)
    hiloCargas.start()
    # Variables globales para control de hilos
    global alimentacion
    global envioDB
    global power
    # Inicio de Hilo para guardar los datos leidos en la base de datos
    hiloEnvioDatosBD = thr.Thread(target=obtener_datos)
    hiloEnvioDatosBD.setDaemon(True)
    hiloEnvioDatosBD.start()
    power = iniciar_pwm(1000, 100) # No se permite el paso de corriente en el módulo de potencia

    while True:
        if cargarAuto and not cargarBateria:
            print("Cargar Auto")
            # Apagado del switch de carga de la bateria
            io_carga(0)
            # Muerte del Hilo paso de fuentes en ejecución
            alimentacion = False
            time.sleep(60)
            # Creación y activación de un nuevo hilo de paso de fuentes
            hiloPasoFuente = thr.Thread(target=paso_fuentes)
            hiloPasoFuente.setDaemon(True)
            hiloPasoFuente.start()
            # lógica del cargador
            if fuente < 2:  # Se carga con aerogenerador o panel solar
                print("Se selecciono la fuente: ", fuente)
                io_bateria(0)
                actualizar_dc(power, 0) # Se permite el paso de corriente en el módulo de potencia
                io_inversor(1)
            elif fuente == 2:  # Se carga con bateria
                print("Se selecciono la bateria")
                actualizar_dc(power, 100) # No se permite el paso de corriente en el módulo de potencia
                io_inversor(1)
                io_bateria(1)
            elif fuente == 3:  # Se carga con energia de CFE
                print("Se selecciono CFE: ")
                actualizar_dc(power, 100) # No se permite el paso de corriente en el módulo de potencia
                io_inversor(0)
                io_bateria(0)
        elif cargarBateria and not cargarAuto:
            print("Cargar Bateria")
            # Apagado de switches del inversor y descarga de bateria
            io_bateria(0)
            io_inversor(0)
            # Muerte del Hilo paso de fuentes en ejecución
            alimentacion = False
            time.sleep(60)
            # Creación y activación de un nuevo hilo de paso de fuentes
            hiloPasoFuente = thr.Thread(target=paso_fuentes)
            hiloPasoFuente.setDaemon(True)
            hiloPasoFuente.start()
            # Lógica de la carga de la bateria
            if fuente > 2:  # Solo se carga con panel solar o aerogenerador
                if float(lecturaPIC[2]) >= BATERIA_CARGADA:
                    print("Bateria cargada")
                    actualizar_dc(power, 100) # No se permite el paso de corriente en el módulo de potencia
                    io_carga(0)
                    cargarBateria = False
                else:
                    print("Iniciando carga de bateria")
                    io_inversor(0)
                    io_bateria(0)
                    io_carga(1)
                    actualizar_dc(power, 0) # Se permite el paso de corriente en el módulo de potencia
        elif not cargarBateria and not cargarAuto:
            # No hay elementos que requieran carga
            print("Rutina de descanso")
            # Muerte del Hilo paso de fuentes en ejecución
            alimentacion = False
            time.sleep(60)
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
    cerrar_conexion_serial(conSerial)
    apagar_fuentes()
    cargarAuto = False
    cargarBateria = False
    alimentacion = False
    envioDB = False
    parar_pwm(power)
    time.sleep(65)
    GPIO.cleanup()
