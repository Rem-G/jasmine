import pymongo
from credentials import CONNECTION_STRING
from bson.objectid import ObjectId

class ClientDB:
    client = pymongo.MongoClient(CONNECTION_STRING)
    db = client.jasmine

    def import_document(self, collection, document):
        collec = self.db[collection]
        return collec.insert_one(document).inserted_id

    def get_tweets_by_date(self, collection, date):
        collec = self.db[collection]
        return collec.find({"date": date})

    def get_tweets_by_id(self, collection, id):
        collec = self.db[collection]
        return collec.find_one({"_id": ObjectId(id)})