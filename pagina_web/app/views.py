from django.shortcuts import render
import pymongo
import json
def inicio(request):
    return render(request, 'home.html')

def dashboard(request):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["Prueba_cargador"]
    #Graphic Batery
    collection = db["Mediciones"]
    # Consulta de datos desde MongoDB
    data1 = collection.find_one({}, {"_id": 0, "voltaje Inversor": 0 ,"intensidad Entrada":0,"intensidad Inversor":0,"temperatura Bateria":0, "Carga Bateria":0})
    data2 = collection.find_one({},{"_id": 0, "voltaje Panel Solar":0, "voltaje Aerogenerador":0, "voltaje Bateria":0, "voltaje CFE":0, "voltaje Inversor": 0 ,"intensidad Entrada":0,"intensidad Inversor":0})
    
    #data_list = list(data)
    #Grapich fuentes
    pie_data = []

    for key, value in data1.items():
     pie_data.append({
        "label": key,
        "value": value
    })
    data1_json = json.dumps(pie_data)
    
    #Grapich Bateria
    pie_data2 = []

    for key, value in data2.items():
     pie_data2.append({
        "label": key,
        "value": value
    })
    data2_json = json.dumps(pie_data2)
    return render(request, 'dashboard.html', {'data1_json': data1_json, 'data2_json': data2_json})


    


