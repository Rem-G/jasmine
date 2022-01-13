import pymongo
from .credentials import CONNECTION_STRING
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
    
    def get_document_one(self, collection, name, value):
        collec = self.db[collection]
        return collec.find_one({name: value})
        
    def import_document(self, collection, document):
        collec = self.db[collection]
        return collec.insert_one(document).inserted_id

    def get_all(self, collection):
        ar = []
        collec = self.db[collection]
        for i in collec.find({}):
            ar.append(i)
        return ar
    
    def get_tweets(self, collection, name, resarch):
        collec = self.db[collection]
        return collec.find({name: resarch})

    def between_date(self, collection, name, gte, lt):
        collec = self.db[collection] 
        return collec.find({
            name: {"$lt": lt, "$gte": gte}
        })
        
if __name__ == "__main__":
    db = ClientDB()
    testdata = {"test":"bonjour"}
    db.import_document("test", testdata)