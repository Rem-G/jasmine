from src.twitter_scraper import TwitterScraper

test = TwitterScraper(headless=False)
test.crawl_historical_tweets("bitcoin", min_faves=100, min_retweets=28, min_replies=0, since="2021-01-01", to="now", step=2)