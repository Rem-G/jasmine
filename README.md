
# Jasmine
The aim of this project is to obtain a trend on the bitcoin price using the various tweets on the subject. 
To do this, you need to have access to the tweeter APIs and put the keys and tokens in the file src/services/credentials.py

To retrieve the tweets for the test set we cannot use the api and the search_full_archive functionality directly as it is paid for and highly limited.
In a first step we will try to retrieve the most influential users in the bitcoin sector. 
Then we will retrieve the timeline of the users, the twitter api limits us to 3000 items including tweets, rt and quote.

## Source files

- bull_bear_analysis.py => create bull/bear model

- compute_sentiment.py => create sentiment model

- find_tweets_by_api.py => Find time line and add tweets in database

- generated_df.py => Generated a dataframe from database

- generated_json.py => Generated a json file from database

- get_tweets.py => Get tweets from a user by vip API

- influent_account.py => Find and add to database influent account

- sentiment_analysis.py => Compute sentiment analysis

- twitter_scraper.py => Twitter scraper

- processing_data => code used to create the json used for machine learning

crypto_evolution.py => retrieves a collection of tweets in db and adds to each document the price/volume evolution before and after the tweet (with a defined period)


# Dataset pre-treatment and model learning

The dataset pre-treatment and the machine learning model were made in the following Google Colab :

https://colab.research.google.com/drive/1kVmyS-41VosikUBkm-n6Q533BKpy4zrg?usp=sharing


