import tweepy
from tweepy.api import API
from credentials import TWITTER_ACCESS_TOKEN_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_API_KEY, TWITTER_API_KEY_SECRET

class Client():
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    def get_api(self):
        return self.api
