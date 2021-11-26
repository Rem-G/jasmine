import tweepy
from credentials import *
import importlib
from scraper import Scrap

class Whales:
    def __init__(self, topic):
        self.topic = topic
        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth)

    def get_initial_tweets(self):
        for tweet in tweepy.Cursor(self.api.search_tweets, q='tweepy').items(10):
            print(tweet.text)

        for tweet in tweepy.Cursor(self.api.search_tweets, q=self.topic, until="2015-01-01").items():
            print(tweet.text)

        tweets = self.api.search_tweets(q=self.topic, count=1000, until="2015-01-01")
        print(tweets)


    def test(self):
        scraper = Scrap(remote=False, headless=True)
        print(scraper.get("https://twitter.com"))



if __name__ == "__main__":
    whales = Whales("bitcoin")
    whales.test()



    