import serial

SERIAL_PORT = "/dev/ttyS0" # "/dev/ttyAMA0" o "/dev/ttyS0"
BYTES_LECTURA = 2

def crear_conexion_serial():
    conexion = serial.Serial(SERIAL_PORT, 9600, timeout= 1)
    return conexion
    

def envio_valores(conexion,valores):
    data = bytes(valores,'utf-8')
    if conexion.write(data):
        return "Se envio con exito"
    return "Vuelve a intentarlo"


def leer_valores(conexion):
    return conexion.read(BYTES_LECTURA)

def cerrar_conexion(conexion):
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
    envio_valores(con,"Hola mundo")
    lectura = leer_valores(con)
    print(lectura,type(lectura))
    cerrar_conexion(con)
except SerialException:
    print("Ocurrio un error en el envio o lectura de datos")
except SerialTimeoutExceptio:
    print("Tiempo de espera superado")



