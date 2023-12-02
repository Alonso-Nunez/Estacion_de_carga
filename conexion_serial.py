import time
import serial
import struct

SERIAL_PORT = "/dev/ttyS0"  # "/dev/ttyS0"  "/dev/ttyAMA0" o "/dev/ttyS0"
BYTES_LECTURA = 2
VOLTAJE_RESOLUCION = 5/1023


def crear_conexion_serial():
    """
    Crea una conexion utilizando el puerto serial

    Returns:
        conexion (objet): Objeto de la conexion creada
    """
    conexion = serial.Serial(SERIAL_PORT, 9600, timeout=10)
    return conexion


def envio_valores(conexion, valores):
    """
    Función que envia datos por el puerto serial

    Args:
        conexion (object): Objeto de la conexion a enviar los valores
        valores (string): Cadena a enviar por el puerto serial

    Returns:
        boolean: Estado del exito del envio de datos
    """
    data = bytes(valores, 'utf-8')
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
    return conexion.read(BYTES_LECTURA)


def cerrar_conexion_serial(conexion):
    """
    Función que cierra la conexion del puerto serial

    Args:
        conexion (object): Objeto de la conexion a cerrar
    """
    conexion.close()


try:
    global con
    con = serial.Serial(SERIAL_PORT, baudrate=9600, timeout=1)
    while True:
        envio_valores(con, input("Escribe el valor a leer "))
        lectura = leer_valores(con)
        lectura_i = int.from_bytes(lectura, byteorder='big')
        print(lectura_i, type(lectura_i))
        voltaje = float(lectura_i)*VOLTAJE_RESOLUCION
        print(lectura, type(lectura), len(lectura))
        print(str(voltaje))
        time.sleep(0.5)

except serial.SerialException as err:
    print("Ocurrio un error en el envio o lectura de datos", err)
except serial.SerialTimeoutException as error:
    print("Tiempo de espera superado", error)
finally:
    cerrar_conexion_serial(con)
