from nltk.util import pr
from service.client_twitter import Client
import numpy
import tweepy
from service.client_mongodb import ClientDB
import time
'''
To start searching for tweets we need to set two important variables. 
The first variable is the important accounts from where the search will start, the second is the keywords.
'''

class Study_account:
    list_of_folower = []
    list_of_friends = []
    mean_of_folower_followers = 0
    mean_of_friends_followers = 0
    is_verif = False
    my_folowers = 0
    def __init__(self, name, keyword) -> None:
        self.keyword = keyword
        self.name = name
        self.client = Client().get_api()

    def get_account(self) -> list:
        return self.client.get_user(screen_name = self.name)

    def evaluate_profile(self) -> bool:
        profile_score = 0
        profile = self.get_account()
        profile_json = profile._json
        self.my_folowers = profile_json["followers_count"]
        self.is_verif = profile_json["verified"]
        profile_score = (self.is_verif * 10) + (self.my_folowers / 707) #707 is a avg of follower for a account in twitter 
        if any(keyw in profile_json["description"] for keyw in self.keyword):
            profile_score += 10
        apparition, nbr_rt, nbr_like = self.mean_of_interaction(100)
        profile_score += apparition * 10
        profile_score += nbr_rt * 5 + nbr_like/2
        folower, mean_fo = self.liste_of_folower_name(100)
        friends, mean_fi = self.liste_of_friends_name(100)
        self.list_of_folower = folower
        self.list_of_friends = friends
        self.mean_of_folower_followers = mean_fo
        self.mean_of_friends_followers = mean_fi
        profile_score += mean_fo * 1.5
        profile_score += mean_fi * 0.1
        return profile_score

    def mean_of_interaction(self, nbr):
        time_line = self.client.user_timeline(screen_name = self.name, count = nbr)
        sum_of_keyword_apparition, list_of_like, list_of_rt = 0, [], []
        
        for tweet in time_line:
            value = tweet._json
            if any(keyw in value["text"] for keyw in self.keyword):
                sum_of_keyword_apparition += 1
        
            list_of_rt.append(value["retweet_count"])
            list_of_like.append(value["favorite_count"])
        
        return sum_of_keyword_apparition, numpy.mean(list_of_rt), numpy.mean(list_of_like)

    def liste_of_folower_name(self, nbr = numpy.infty):
        folower_screen_name = []
        folower_folower_avg = []
        for page in tweepy.Cursor(self.client.get_followers, screen_name=self.name).pages():  
            for people in page:
                if len(folower_screen_name) <= nbr:
                    folower_screen_name.append(people._json["screen_name"])
                    folower_folower_avg.append(people._json["followers_count"])
                else:
                    return folower_screen_name, numpy.mean(folower_folower_avg)
        return folower_screen_name, numpy.mean(folower_folower_avg)
    
    def liste_of_friends_name(self, nbr = numpy.infty):
        friends_screen_name = []
        friends_folower_avg = []
        for page in tweepy.Cursor(self.client.get_friends, screen_name=self.name).pages():  
            for people in page:
                if len(friends_screen_name) <= nbr:
                    friends_screen_name.append(people._json["screen_name"])
                    friends_folower_avg.append(people._json["followers_count"])
                else:
                    return friends_screen_name, numpy.mean(friends_folower_avg)
        return friends_screen_name, numpy.mean(friends_folower_avg)
    
    def get_result(self):
        final_score = self.evaluate_profile()
        return final_score,self.my_folowers, self.is_verif, self.list_of_folower, self.list_of_friends, self.mean_of_folower_followers, self.mean_of_friends_followers

class Resarch_people:
    def __init__(self, listOfNextResarch, keyWord) -> None:
        self.listOfResarch = listOfNextResarch
        self.keyWord = keyWord
        self.clientDB = ClientDB()

    def processing_for_on(self):
        inDb = self.clientDB.get_document_one("user", "name", self.listOfResarch[0])
        if ( inDb == None):
            fia = Study_account(self.listOfResarch[0], self.keyWord)
            score, folower, verif, list_fo, list_fri, mean_my_fo_fo, mean_fr_fo = fia.get_result()       
            if score > 1000:
                data = {"name": self.listOfResarch[0], "score": score, "follower": folower, "certif_account": verif, "follower_mean_follower": mean_my_fo_fo, "friends_mean_follower": mean_fr_fo }
                print(f"The score is {score}")
                self.clientDB.import_document('user', data) 
                self.listOfResarch.extend(list_fri)
                # self.listOfResarch.extend(list_fo)            
        else:
            print("Alredy in data base")
    def processing(self):
        while len(self.listOfResarch) > 0:
            print("Find for : " + self.listOfResarch[0])
            self.processing_for_on()
            del self.listOfResarch[0]

if __name__ == "__main__":
    INITIAL = ["@Bitcoin", "@BitcoinSVNode", "@BTCFoundation", "@BTCTN", "@cz_binance", "@crypto", ""]
    KEYWORD = ["Bitcoin", "Btc", "₿", "Crypto", "bitcoin", "btc", "crypto", "BTC"]
    Resarch_people(INITIAL, KEYWORD).processing()
