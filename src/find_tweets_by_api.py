import re
import time
from nltk.util import pr
from numpy import e
from pymongo.common import validate_ok_for_replace
from service.client_mongodb import ClientDB
from service.client_twitter import Client
import tweepy
from datetime import datetime
# Variable
ClientDB = ClientDB()
clientTW = Client().get_api()
TableDB = "tweets_api"

class TweetFinder:
    def __init__(self, name) -> None:
        self.name = name
    
    def save_tweet_bis(self):
        for tweets in tweepy.Cursor(clientTW.user_timeline, screen_name=self.name, exclude_replies =True, include_rts = False).pages():  
            for tweet in tweets:
                value = tweet._json
                if ClientDB.get_document_one(TableDB, "id_str", value["id_str"]) == None:
                    ClientDB.import_document(TableDB, {"name": value["user"]["screen_name"], "text": value["text"], "id_str": value["id_str"], "created_at": value["created_at"], "retweet_count": value["retweet_count"], "favorite_count": value["favorite_count"]})
                else:
                    print("Deja dans la base de données")
                    return

if __name__ == "__main__":
    all_people = ClientDB.get_all("influent_bitcoin_account")
    print("Fin de la récupération des utilisateurs")
    for i in all_people:
        try:
            print("search for " + i["name"])
            TweetFinder(i["name"]).save_tweet_bis()
        except Exception:
            pass

# BTCFoundation
