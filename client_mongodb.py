import pymongo
from client_twitter import Client
from credentials import CONNECTION_STRING

class ClientDB:
    client = pymongo.MongoClient(CONNECTION_STRING)
    db = client.jasmine

    def import_document(self, document, collection):
        myDataBase = self.db[collection]
        return myDataBase.insert_one(document).inserted_id
