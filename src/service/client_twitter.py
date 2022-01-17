import tweepy
from tweepy import api
from .credentials import TWITTER_ACCESS_TOKEN_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_API_KEY, TWITTER_API_KEY_SECRET, TWITTER_AUTH, TWITTER_PREMIUM
import random
class Client():
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth,  wait_on_rate_limit=True)

    def get_api(self):
        return self.api
    def stream(self, stream_listener):
        return tweepy.Stream(auth=api.auth, listener=stream_listener)

class MultipleClients():
    Twitter_env = ""
    def get_new_auth(self, keys_num = None, isVIP = False):
        try:
            if (isVIP):
                if (keys_num == None):
                    ran = random.randint(0,len(TWITTER_PREMIUM)-1)
                    keys = TWITTER_PREMIUM[ran]
                    self.Twitter_env = keys["TWITTER_ENV"]
                else:
                    keys = TWITTER_PREMIUM[keys_num]
                    self.Twitter_env = keys["TWITTER_ENV"]
            else:
                if (keys_num == None):
                    keys = TWITTER_AUTH[random.randint(0,len(TWITTER_AUTH)-1)]
                else:
                    keys = TWITTER_AUTH[keys_num]
            print(f'Use api {keys["TWITTER_API_KEY"]}')
            auth = tweepy.OAuthHandler(keys["TWITTER_API_KEY"], keys["TWITTER_API_KEY_SECRET"])
            auth.set_access_token(keys["TWITTER_ACCESS_TOKEN"], keys["TWITTER_ACCESS_TOKEN_SECRET"])
            api = tweepy.API(auth,  wait_on_rate_limit=True)
            return api
        except Exception as e:
            print("Api Keys do not work retry with an other")
            print(e)
            self.get_new_auth()

    def get_env(self):
        return self.Twitter_env