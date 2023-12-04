from django.shortcuts import render
import pymongo
import json
import time


def inicio(request):
    return render(request, 'home.html')


def dashboard(request):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["Prueba_cargador"]
    # Graphic Batery
    collection = db["Mediciones"]
    # Recupera todos los documentos de la colección
    # Graphic fuentes
    documentos = list(collection.find({}, {"_id": 0,
                                           "V_Inversor": 0,
                                           "I_Entrada": 0,
                                           "I_Inversor": 0,
                                           "Carga_Bateria": 0}))

    # Grapich Bateria
    documentos1 = list(collection.find({}, {"_id": 0,
                                            "voltaje_Inversor": 0,
                                            "intensidad_Entrada": 0,
                                            "intensidad_Inversor": 0,
                                            "Carga_Bateria": 0}))

    # Graphic intensidad
    documentos2 = list(collection.find({}, {"_id": 0,
                                            "voltaje_Inversor": 0,
                                            "temperatura_Bateria": 0,
                                            "Carga_Bateria": 0}))

    return render(request, 'dashboard.html', {'documentos': documentos, 'documentos1': documentos1, 'documentos2': documentos2})
