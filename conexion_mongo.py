import pymongo

MONGO_HOST = "localhost"
MONGO_PUERTO = "27017"
MONGO_TIMEOUT = 1000
MONGO_URL = "mongodb://" + MONGO_HOST + ":" + MONGO_PUERTO + "/"
ID_REGISTRO = ""

MONGO_BD = "Prueba_cargador"
MONGO_COLECCION = "Bateria"  # "Entradas""Salida"


def conectar_db(base_datos, bd_coleccion):
    cliente = pymongo.MongoClient(MONGO_URL, serverSelectionTimeoutMS=MONGO_TIMEOUT)
    base = cliente[base_datos]
    coleccion = base[bd_coleccion]
    return cliente, coleccion