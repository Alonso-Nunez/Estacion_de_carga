from django.shortcuts import render
import pymongo
import json
def inicio(request):
    return render(request, 'home.html')

def dashboard(request):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["db_prueba"]
    #Graphic Batery
    collection = db["Bateria"]
    # Consulta de datos desde MongoDB
    data = collection.find_one({}, {"_id": 0})
    #data_list = list(data)
    pie_data = []

    for key, value in data.items():
     pie_data.append({
        "label": key,
        "value": value
    })
    data_json = json.dumps(pie_data)
    return render(request, 'dashboard.html', {'data_json': data_json})


