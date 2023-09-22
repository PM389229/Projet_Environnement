from fastapi import FastAPI, Query
from flask import jsonify
from pymongo import MongoClient

app = FastAPI()

client = MongoClient("mongodb://root:example@localhost:27017/")
db = client["Environnement"]
collection = db["Environnement_c"]

# Endpoint pour récupérer toutes les données
@app.get("/api/data")
async def get_all_data():
    data = list(collection.find({}, {"_id": 0}))
    return data

@app.get("/api/data/{region}")
async def get_data_by_region(region: str):
    data = collection.find({"Region": region}, {"_id": 0})
    data = list(data)  # Convertissez le curseur en liste
    # Convertissez les ObjectId en str pour les rendre JSON sérialisables
    data = [{**item, '_id': str(item.get('_id'))} for item in data]
    return data