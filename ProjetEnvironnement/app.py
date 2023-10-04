#Import des bibliothèques nécessaires 
#On initialise une instance FastAPI en créant un objet app
from fastapi import FastAPI, Query
from flask import jsonify
from pymongo import MongoClient

app = FastAPI()

#On crée une connecion à la base de données mongo avec pymongo
client = MongoClient("mongodb://root:example@localhost:27017/")
db = client["Environnement"]
collection = db["Environnement_c"]


#On crée un endpoint GET /api/data qui renvoie toutes les données de la collection Environnement_c sans l'ID 
#Les données sont retournées au format JSON.
@app.get("/api/data")
async def get_all_data():
    data = list(collection.find({}, {"_id": 0}))
    return data

#L'Endpoint GET 'api/data/{region}' suivant récupère les données par région
#On utilise collection.find pour récupérer les données de la région demandée sans l'ID 
#Ces données par région demandée sont converties en listes et on convertit les ObjectID 
#en chaines(str) pour les rendre JSON serialisables
@app.get("/api/data/{region}")
async def get_data_by_region(region: str):
    data = collection.find({"Region": region}, {"_id": 0})
    data = list(data) 
    data = [{**item, '_id': str(item.get('_id'))} for item in data]
    return data


#Pour résumer C'est la structure générale de mon application FastAPI 
#qui permet de récupérer des données depuis la base de données MongoDB en utilisant des endpoints RESTful.