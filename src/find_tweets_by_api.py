import os
from nltk.util import pr
from numpy import e
from pymongo.common import validate_ok_for_replace
from service.client_mongodb import ClientDB
from service.client_twitter import Client
import tweepy
from datetime import datetime
import pickle
# Variable
ClientDB = ClientDB()
clientTW = Client().get_api()
TableDB = "tweets"

class TweetFinder:
    def __init__(self, name) -> None:
        self.name = name
    
    def save_tweet_bis(self):
        inputValue = 0
        for tweets in tweepy.Cursor(clientTW.user_timeline, screen_name=self.name, include_rts = False, exclude_replies = True).pages():  
            for tweet in tweets:
                value = tweet._json
                if ClientDB.get_document_one(TableDB, "id_str", value["id_str"]) == None:
                    inputValue += 1
                    refactor_date = datetime.strptime(value["created_at"], "%a %b %d %H:%M:%S +%f %Y")
                    ClientDB.import_document(TableDB, {"name": value["user"]["screen_name"], "text": value["text"], "id_str": value["id_str"], "created_at": refactor_date, "retweet_count": value["retweet_count"], "favorite_count": value["favorite_count"]})
                else:
                    print("Un tweets de l'utilisateur est daja dans la base de données, cahngement d'utilisateur")
                    return -1
        return inputValue

def read_save(path, name):
    if name in os.listdir(path):
        with open(f'{path}/{name}', 'rb') as f:
            load = pickle.load(f)
            return load
    else:
        return False

def save_list_search(path, name, data):
    with open(f'{path}/{name}', 'wb') as f:
        pickle.dump(data, f)

if __name__ == "__main__":
    all_people = ClientDB.get_all("influent_bitcoin_account")
    print("Fin de la récupération des utilisateurs")
    number_of_tweets_by_user = read_save("./src/save", "number_of_tweets_by_user")
    if (number_of_tweets_by_user == False):
        number_of_tweets_by_user = {}
    print("Début de la récupération")
    for i in all_people:
        try:
            print("search for " + i["name"])
            number_of_tweets_by_user[i["name"]] = TweetFinder(i["name"]).save_tweet_bis()
            save_list_search("./src/save", "number_of_tweets_by_user", number_of_tweets_by_user)

        except Exception as e:
            print(f'Error for : {i["name"]} ==> {e}')
            number_of_tweets_by_user[i["name"]] = -1
            save_list_search("./src/save", "number_of_tweets_by_user", number_of_tweets_by_user)

    print(number_of_tweets_by_user)
# BTCTN
