import pymongo
import time

MONGO_HOST = "localhost"
MONGO_PUERTO = "27017"
MONGO_TIMEOUT = 1000
MONGO_URL = "mongodb://" + MONGO_HOST + ":" + MONGO_PUERTO + "/"
ID_REGISTRO = ""

MONGO_BD = "Prueba_cargador"
MONGO_COLECCION = "Mediciones"


def conectar_db(base_datos, bd_coleccion):
    """
    Función de conexion con la base de datos

    Args:
        base_datos (string): Base de datos a la cual se conecta
        bd_coleccion (string): Coleccion a la cual se conecta el cliente para crear documentos

    Returns:
        cliente object: conexion establecida genera un cliente
        coleccion object: coleccion a la que se conecto, ayuda a verificar si la conexion fue hecha correctamente
        base object:ayuda a berificar si la conexion fue exitosa
    """
    try:
        cliente = pymongo.MongoClient(MONGO_URL, serverSelectionTimeoutMS=MONGO_TIMEOUT)
        base = cliente[base_datos]
        coleccion = base[bd_coleccion]
        print("Conexion establecida en "+str(coleccion))
        return cliente, coleccion
    except pymongo.errors.ServerSelectionTimeotError as error:
        print("Error con la conexion de la base "+error)
    except pymongo.errors.ConnectionFailure as error:
        print("No se pudo conectar con mongo "+error)


def desconectar_db(cliente):
    """
    Función de desconexión con la base de datos

    Args:
        cliente (object): cliente a cerrar
    """
    cliente.close()
    print("Conexion cerrada")

def insertar_datos(datos):
    """
    Funcion que envia datos a la coleccion con la conexion establecida

    Args:
        cliente (object): conexion establecida con la base de datos
        datos (array): arreglo con los datos a guardar
    """
    enviarDatos = {}
    enviarDatos["voltaje Panel Solar"] = datos[0]
    enviarDatos["voltaje Aerogenerador"] = datos[1]
    enviarDatos["voltaje Bateria"] = datos[2]
    enviarDatos["voltaje CFE"] = datos[3]
    enviarDatos["voltaje Inversor"] = datos[4]
    enviarDatos["intensidad Entrada"] = datos[5]
    enviarDatos["intensidad Inversor"] = datos[6]
    enviarDatos["temperatura Bateria"] = datos[7]
    enviarDatos["hora"] = time.localtime()
    print(enviarDatos)
    try:
        conexion, coleccion = conectar_db(MONGO_BD, MONGO_COLECCION)
        coleccion.insert_one(enviarDatos)
        print("Envio de datos exitoso")
    except Exception as error:
        print("Error guardando datos " + str(error))
    finally:
        desconectar_db(conexion)

arreglo = [12,12,12,140,12,3,3,45]
insertar_datos(arreglo)