from contextlib import nullcontext
import os
import pickle

from numpy import array, number
import numpy
import tweepy
from service.client_mongodb import ClientDB
from service.client_twitter import Client

# Variable
ClientDB = ClientDB()
clientTW = Client().get_api()
TableDB = "user_v2"

class Account_scoring:
    def __init__(self, name, key_words, deep, next) -> None:
        self.key_words = key_words
        self.name = name
        self.account = self.get_account()._json
        self.deep = deep
        self.next = next

    def get_account(self) -> list:
        return clientTW.get_user(screen_name = self.name)
    
    def processing_account(self) -> number:
        followers = self.account["followers_count"]
        verified = self.account["verified"]
        description_kw = 0
        friends = self.account["friends_count"]
        if (followers < 500 or followers/friends < 2):
            raise print("Pas assez de folowers")
            
        if any(keyw.upper() in self.account["description"].upper() for keyw in self.key_words):
            description_kw += 1
        score = ((followers - 707) / friends) + (verified * 250) + (description_kw * 100)
        kw_app, mean_rt, mean_like = self.mean_of_interaction()
        score += (kw_app * 10) + (mean_rt * 1.5) + (mean_like * 0.5)
        # next_account = self.list_of_friends_name(self.next)
        next_account = []
        return score, next_account, followers, friends, mean_rt, mean_like, description_kw, kw_app, verified
        
    def mean_of_interaction(self):
            time_line = clientTW.user_timeline(screen_name = self.name, count = self.deep)
            sum_of_keyword_apparition, list_of_like, list_of_rt = 0, [], []
            isKW = 0
            for tweet in time_line:
                value = tweet._json
                if (value["text"][0:2] != "RT"):
                    if any(keyw.upper() in value["text"].upper() for keyw in self.key_words):
                        sum_of_keyword_apparition += 1
                        isKW = 1
                    list_of_rt.append(value["retweet_count"] + (isKW * 20))
                    list_of_like.append(value["favorite_count"] + (isKW * 50))
                    isKW = 0
            return sum_of_keyword_apparition, numpy.mean(list_of_rt), numpy.mean(list_of_like)

    def list_of_friends_name(self, nbr = numpy.infty):
        friends_screen_name = []
        for page in tweepy.Cursor(clientTW.get_friends, screen_name=self.name).pages():  
            for people in page:
                if len(friends_screen_name) <= nbr:
                    friends_screen_name.append(people._json["screen_name"])
                else:
                    return friends_screen_name
        return friends_screen_name

class Search:
    def __init__(self, listOfNextResarch, keyWord) -> None:
        self.save = "./src/save/save_listSearch"
        if self.readSave() != False:
            self.listOfResarch = self.readSave()
        else:
            self.listOfResarch = listOfNextResarch
        self.keyWord = keyWord

    def readSave(self) -> array or False:
        if "save_listSearch" in os.listdir("./src/save"):
            with open(self.save, 'rb') as f:
                users = pickle.load(f)
                print(f'They are {len(users)} in the liste')
                return list(set(users))
        else:
            return False
    
    def saveListSearch(self):
        with open(self.save, 'wb') as f:
            pickle.dump(self.listOfResarch, f)

    def processing_for_on(self) -> None:
        inDb = ClientDB.get_document_one(TableDB, "name", self.listOfResarch[0])
        if ( inDb == None):
            account_processing = Account_scoring(self.listOfResarch[0], self.keyWord, 150, 20)
            score, next_account, followers, friends, mean_rt, mean_like, description_kw, kw_app, verified = account_processing.processing_account()       
            if score > 500:
                data = {"name": self.listOfResarch[0], "score": score, "followers": followers, "friends": friends, "mean_rt": mean_rt, "mean_like": mean_like, "description_kw": description_kw, "kw_app": kw_app, "verified": verified}
                print(f"The score is {score}")
                ClientDB.import_document(TableDB, data) 
                self.listOfResarch.extend(next_account)
        else:
            print("Alredy in data base")

    def processing(self) -> None:
        index = 0
        while len(self.listOfResarch) > 0:
            print("Find for : " + self.listOfResarch[0])
            try:
                self.processing_for_on()
            except Exception as err:
                pass
            del self.listOfResarch[0]
            if (index % 3 == 0):
                self.saveListSearch()
            index+=1 

if __name__ == "__main__":
    KEYWORD = ["Bitcoin", "Btc", "₿", "Crypto", "#Bitcoin", "#Btc", "#₿", "#Crypto"]
    INITIAL = ["@whale_alert"]
    Search(INITIAL, KEYWORD).processing()