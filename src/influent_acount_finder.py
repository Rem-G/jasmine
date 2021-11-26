from service.client_twitter import Client
import numpy
import tweepy
import time
'''
To start searching for tweets we need to set two important variables. 
The first variable is the important accounts from where the search will start, the second is the keywords.
'''
INITIAL = ["@elonmusk", "@Bitcoin", "@BitcoinSVNode", "@BTCFoundation", "@BTCTN", "@cz_binance", "@crypto"]
KEYWORD = ["Bitcoin", "Btc", "₿", "Crypto", "bitcoin", "btc", "crypto"]
class Find_influent_acount:
    def __init__(self, initial, keyword) -> None:
        self.initial = initial
        self.keyword = keyword
        self.client = Client().get_api()

    def get_account(self, name) -> list:
        return self.client.get_user(screen_name = name)

    def evaluate_profile(self, name) -> bool:
        profile_score = 0
        profile = self.get_account(name)
        profile_json = profile._json
        profile_score = (profile_json["verified"] * 10) + (profile_json["followers_count"] / 100000)
        if any(keyw in profile_json["description"] for keyw in self.keyword):
            profile_score += 10

        print(profile_score)

    def mean_of_interaction(self, name, nbr):
        time_line = self.client.user_timeline(screen_name = name, count = nbr)
        sum_of_keyword_apparition, list_of_like, list_of_rt = 0, [], []
        
        for tweet in time_line:
            value = tweet._json
            if any(keyw in value["text"] for keyw in self.keyword):
                sum_of_keyword_apparition += 1
        
            list_of_rt.append(value["retweet_count"])
            list_of_like.append(value["favorite_count"])
        
        return sum_of_keyword_apparition, numpy.mean(list_of_rt), numpy.mean(list_of_like)

    def liste_of_folower_name(self, name, nbr):
        folower_screen_name = []
        for page in tweepy.Cursor(self.client.get_followers, screen_name=name).pages():  
            for people in page:
                if len(folower_screen_name) <= nbr:
                    folower_screen_name.append(people._json["screen_name"])
                else:
                    return folower_screen_name



        return folower_screen_name


fia = Find_influent_acount(INITIAL, KEYWORD)    
# fia.evaluate_profile('@Bitcoin')
print(fia.liste_of_folower_name('@crypto', 10))
