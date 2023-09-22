# Environnement.py
class EnvironnementData:
    def __init__(self, db):
        self.db = db

    def get_all_data(self):
        collection = self.db.get_collection("Environnement_c")
        data = list(collection.find({}))
        return data

    def get_data_by_region(self, region):
        collection = self.db.get_collection("Environnement_c")
        data = list(collection.find({"Region": region}))
        return data