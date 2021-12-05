import pymongo
from src.service.credentials import CONNECTION_STRING
from bson.objectid import ObjectId

class ClientDB:
    def __init__(self):
        self.client = pymongo.MongoClient(CONNECTION_STRING)
        self.db = self.client["jasmine"]

    def insert_documents(self, collection, documents):
        collec = self.db[collection]
        return collec.insert_many(documents)

    def get_tweets_by_date(self, collection, date):
        collec = self.db[collection]
        return collec.find({"dt": date})

    def get_tweets_by_id(self, collection, id):
        collec = self.db[collection]
        return collec.find_one({"_id": ObjectId(id)})