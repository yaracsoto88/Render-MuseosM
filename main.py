import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
import requests
import json 
import random

app=FastAPI()

url="https://services1.arcgis.com/nCKYwcSONQTkPA4K/arcgis/rest/services/MuseosdeMadrid/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json"

def obtener_data_museos():
    #accedemos a la url y guardamos la info en response convirtiendola en formato json
    response=requests.get(url)
    return (response.json())

#función que selecciona un museo aleatoriamente de la lista de museos
def seleccionar_museo_random(data_museos):
    museos = data_museos.get("features", [])
    if not museos:
        return "No se encontraron museos en los datos."
    museo_aleatorio = random.choice(museos)
    atributos = museo_aleatorio.get("attributes", {})
    return json.dumps(museo_aleatorio)


#función para agrupar los museos por barrio
def agrupar_por_barrio(data_museos):
    barrios={}
    #primero recorremos los museos
    for museo in data_museos:
        for museo in data_museos.get("features", {}):
            atributos = museo.get("attributes", {})
            nombre_museo = atributos.get("NOMBRE")
            barrio = atributos.get("BARRIO")
            #si no está el barrio en el dict vacío, crea la posición y añade el museo al barrio correspondiente
            if barrio not in barrios:
                barrios[barrio] = []
                barrios[barrio].append(nombre_museo)
            else:
                barrios[barrio].append(nombre_museo)
                
    return json.dumps(barrios)

#Función para mostrar todos los museos de un mismo distrito
def mostrar_museos_distrito(data_museos, distrito):
    museos = data_museos.get("features", [])
    if not museos:
        return "No se encontraron museos en los datos."

    museos_en_distrito = []
    for museo in museos:
        atributos = museo.get("attributes", {})
        if atributos.get("DISTRITO") == distrito:
            museos_en_distrito.append(museo)

    return json.dumps({"museos_por_distrito": museos_en_distrito})


#invocamos a las funciones
distrito = "CENTRO"
data_museos=obtener_data_museos()
museo_rm=seleccionar_museo_random(data_museos)
barrios_museo=agrupar_por_barrio(data_museos)
museos_en_distrito_centro = mostrar_museos_distrito(data_museos, distrito)


#endpoints
@app.get("/")
async def root():
    file_path=os.path.join("static", "index.html")
    return(FileResponse(file_path))

@app.get("/random_museo")
async def get_random_museo():
    museo_rm=seleccionar_museo_random(data_museos)
    return museo_rm

@app.get("/barrios")
async def get_barrios():
    barrios_museo=agrupar_por_barrio(data_museos)
    return barrios_museo

@app.get("/distrito")
async def get_museo_distrito():
    museos_en_distrito_centro = mostrar_museos_distrito(data_museos, distrito)
    return museos_en_distrito_centro




