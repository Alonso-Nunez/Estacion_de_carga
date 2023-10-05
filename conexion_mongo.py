import pymongo

MONGO_HOST = "localhost"
MONGO_PUERTO = "27017"
MONGO_TIMEOUT = 1000
MONGO_URL = "mongodb://" + MONGO_HOST + ":" + MONGO_PUERTO + "/"
ID_REGISTRO = ""

MONGO_BD = "Prueba_cargador"
MONGO_COLECCION = "Bateria"  # "Entradas""Salida"


def conectar_db(base_datos, bd_coleccion):
    """
    Función de conexion con la base de datos

    Args:
        base_datos (string): Base de datos a la cual se conecta
        bd_coleccion (string): Coleccion a la cual se conecta el cliente para crear documentos

    Returns:
        cliente _type_: conexion establecida genera un cliente
        coleccion _type_: coleccion a la que se conecto, ayuda a verificar si la conexion fue hecha correctamente
        base _type_:ayuda a berificar si la conexion fue exitosa
    """
    cliente = pymongo.MongoClient(MONGO_URL, serverSelectionTimeoutMS=MONGO_TIMEOUT)
    base = cliente[base_datos]
    coleccion = base[bd_coleccion]
    return cliente, coleccion, base