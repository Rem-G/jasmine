from src.twitter_scraper import TwitterScraper
from src.service.client_mongodb import ClientDB
import numpy as np

class Main:
    def __init__(self):
        self.client_db = ClientDB()

    def test(self):
        test = TwitterScraper(headless=False, account=True)
        # collection = self.client_db.get_collection("influent_bitcoin_account")
        # likes = []
        # rt = []
        # for tweet in collection:
        #     likes.append(tweet["mean_like"])
        #     rt.append(tweet["mean_rt"])

        test.crawl_historical_tweets("bitcoin", min_faves=0, min_retweets=0, min_replies=0, account="@elonmusk", since="2017-09-01")

if __name__ == "__main__":
    Main().test()

# test = TwitterScraper(headless=False, account=True)
# # test.crawl_historical_tweets("bitcoin", min_faves=100, min_retweets=28, min_replies=0, since="2017-09-01", to="now", step=2)
# test.crawl_historical_tweets("bitcoin", since="2017-09-01")
