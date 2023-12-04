from Programas_circuitos.conexion_serial import *

try:
    global con
    con = serial.Serial(SERIAL_PORT, baudrate=9600, timeout=1)
    while True:
        print(envio_valores(con, "Hola mundo"))
        lectura = leer_valores(con)
        print(lectura, type(lectura))
        time.sleep(0.5)

except serial.SerialException as err:
    print("Ocurrio un error en el envio o lectura de datos", err)
except serial.SerialTimeoutException as error:
    print("Tiempo de espera superado", error)
finally:
    cerrar_conexion_serial(con)
