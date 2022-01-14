from pymongo.message import query
from service.client_twitter import MultipleClients
from service.client_mongodb import ClientDB
import tweepy
from datetime import datetime

ClientDB = ClientDB()
TableDB = "tweets"

class Get_tweets:
    api = MultipleClients.get_new_auth(0)
    number_of_api_call = 1
    env = ""
    clients = MultipleClients()
    def check(self):
        self.number_of_api_call += 1
        if self.number_of_api_call%2 == 0:
            self.api = self.clients.get_new_auth(0)
    
    def processign(self, user):
        for tweets in tweepy.Cursor(self.api.search_full_archive, label = self.clients.get_env(), query = f'bitcoin (from:{user})').pages():  
            for tweet in tweets:
                value = tweet._json
                if ClientDB.get_document_one(TableDB, "id_str", value["id_str"]) == None:
                    refactor_date = datetime.strptime(value["created_at"], "%a %b %d %H:%M:%S +%f %Y")
                    ClientDB.import_document(TableDB, {"name": value["user"]["screen_name"], "text": value["text"], "id_str": value["id_str"], "created_at": refactor_date, "retweet_count": value["retweet_count"], "favorite_count": value["favorite_count"]})
        self.check()
