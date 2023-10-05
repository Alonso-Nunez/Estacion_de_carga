import serial
import time

SERIAL_PORT ="/dev/ttyAMA0" #"/dev/ttyS0"  "/dev/ttyAMA0" o "/dev/ttyS0"
BYTES_LECTURA = 2

def crear_conexion_serial():
    """
    Crea una conexion utilizando el puerto serial

    Returns:
        conexion (objet): Objeto de la conexion creada
    """
    conexion = serial.Serial(SERIAL_PORT, 9600, timeout= 1)
    return conexion
    

def envio_valores(conexion,valores):
    """
    Función que envia datos por el puerto serial

    Args:
        conexion (object): Objeto de la conexion a enviar los valores
        valores (string): Cadena a enviar por el puerto serial

    Returns:
        boolean: Estado del exito del envio de datos
    """
    data = bytes(valores,'utf-8')
    if conexion.write(data):
        return True
    return False


def leer_valores(conexion):
    """
    Función que leer datos del puerto serial

    Args:
        conexion (object): Objeto de la conexion a leer los datos

    Returns:
        leectura (byte): bytes leidos del puerto serial
    """
    #return conexion.read(BYTES_LECTURA)
    return conexion.readLine()


def cerrar_conexion_serial(conexion):
    """
    Función que cierra la conexion del puerto serial

    Args:
        conexion (object): Objeto de la conexion a cerrar
    """
    conexion.close()
    
    
# Enable Serial Communication
#port = serial.Serial(SERIAL_PORT, baudrate=9600, timeout=1)
#data = bytes('Información serial\n\r','utf-8')
#port.write(data)#Envia información
#dato = port.read(10) #Lee 10 bytes
#port.readline() #Lee toda una linea
#print (data)
#port.close()
try:
    con=crear_conexion_serial()
    envio_valores(con,"Hola mundo desde rasp")
    lectura = leer_valores(con)
    print(lectura,type(lectura))
    cerrar_conexion_serial(con)
    
except SerialException:
    print("Ocurrio un error en el envio o lectura de datos")
except SerialTimeoutExceptio:
    print("Tiempo de espera superado")



