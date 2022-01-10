import tweepy
from tweepy import api
from .credentials import TWITTER_ACCESS_TOKEN_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_API_KEY, TWITTER_API_KEY_SECRET

class Client():
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth,  wait_on_rate_limit=True)

    def get_api(self):
        return self.api
    def stream(self, stream_listener):
        return tweepy.Stream(auth=api.auth, listener=stream_listener)