import json
import re
import string
import os
import numpy as np
import pandas as pd
import nltk
from nltk import FreqDist
from nltk.corpus import stopwords, twitter_samples
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk import classify
from nltk import NaiveBayesClassifier
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from transformers import pipeline
import datetime
import pymongo
import pickle
from river import ensemble
from river import evaluate
from river import metrics
import json
import multiprocessing as mp

nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

def readSave(path, name):
    if name in os.listdir(path):
        with open(f'{path}/{name}', 'rb') as f:
            load = pickle.load(f)
            return load
    else:
        return False

def remove_noise(tweet_tokens, stop_words = ()):
    cleaned_tokens = []
    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                    '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

def classify_naive_bayes(text, model):
    custom_tokens = remove_noise(word_tokenize(text))
    estimation = model.prob_classify(dict([token, True] for token in custom_tokens))
    return estimation.prob("Negative"), estimation.prob("Positive")

class Sentiment:
    def __init__(self, model_nb, model_transformers, model_sentiment_intensity) -> None:
        self.classifer_naive_bayes = model_nb
        self.classifier_transformers = model_transformers
        self.classifer_sentiment_intensity = model_sentiment_intensity

    def classify_sentiment_intensity_analyzer(self, texts):
        pos, neg, neu = 0, 0, 0
        if len(texts) == 0:
            return 0, 0
        for text in texts:
            pos += self.classifer_sentiment_intensity.polarity_scores(text)['pos']
            neg += self.classifer_sentiment_intensity.polarity_scores(text)['neg']
            neu += self.classifer_sentiment_intensity.polarity_scores(text)['neu']
        return (neg + (neu/2))/len(texts), (pos + (neu/2))/len(texts)

    def classify_transformers(self, texts):
        if len(self.classifier_transformers(texts)) == 0:
            return 0,0
        result = self.classifier_transformers(texts)[0]
        if result["label"] == "POSITIVE":
            return 1- result["score"], result["score"]
        return result["score"], 1- result["score"]

    def classify_naive_bayes(self, texts):
        neg, pos = [], []
        if len(texts) == 0:
            return 0,0
        for text in texts :
            val = classify_naive_bayes(text, self.classifer_naive_bayes)
            neg.append(val[0])
            pos.append(val[1])
        return np.mean(neg), np.mean(pos)

    def get_all_mean(self, texts):
        s3 = self.classify_naive_bayes(texts)
        s1 = self.classify_sentiment_intensity_analyzer(texts)
        s2 = self.classify_transformers(texts)
        return {"neg" : (s1[0] + s2[0] + s3[0])/3, "pos": (s1[1] + s2[1] + s3[1])/3}

model = readSave(".", "classifer_sentiment")
classifier_transformers = pipeline('sentiment-analysis')
classifer_sentiment_intensity = SentimentIntensityAnalyzer()
sentiment = Sentiment(model, classifier_transformers, classifer_sentiment_intensity)

dt_end = datetime.datetime.strptime("2022-01-10", "%Y-%m-%d")
dt_start = datetime.datetime.strptime("2019-01-01", "%Y-%m-%d")
dataset = []
dt = dt_start
with open("df.pickle", "rb") as f:
    df = pickle.load(f)
df['created_at'] = pd.to_datetime(df['created_at'])
df_date = pd.read_csv("./BTC-USD.csv", delimiter=",")
df_date["Date"] = pd.to_datetime(df_date['Date'])

list_date = []
while dt < dt_end:
    list_date.append(dt)
    dt += datetime.timedelta(hours=24)

def processing_for_one_date(date): 
    mask = (df['created_at'] > date) & (df['created_at'] <= date + datetime.timedelta(hours=24))
    tweets = df.loc[mask]
    days_value_plus_24 = df_date.loc[df_date['Date'] == date + datetime.timedelta(hours=24)]
    days_value_moins_24 = df_date.loc[df_date['Date'] == date + datetime.timedelta(hours=-24)]
    text,fav, rt,n  = [], 0, 0,0
    for _, tweet in tweets.iterrows():
        fav += int(tweet["favorite_count"])
        rt += int(tweet["retweet_count"])
        n += 1
        text.append(tweet["text"])

    btc_evol_after = (days_value_plus_24['Close'] - days_value_plus_24['Open'])/days_value_plus_24['Open']
    btc_evol_before = (days_value_moins_24['Close'] - days_value_moins_24['Open'])/days_value_moins_24['Open']
    val = {
        "btc_evol_before": btc_evol_before,
        "btc_evol_after": btc_evol_after,
        "sentiment_pos": sentiment.get_all_mean(text)["pos"],
        "fav": fav,
        "rt": rt,
        "n_tweets": n
    }
    with open(f"./data/dataset_{date}.json", 'r') as f:
        dataset = json.load(f)

    
nbr_cpu =  mp.cpu_count()
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
        
chunks = chunks(list_date, nbr_cpu)
pool = mp.Pool(nbr_cpu)
pool.map(processing_for_one_date, [chunk for chunk in chunks])
pool.close()

result = []
for f in os.listdir("./data"):
    with open(f, "rb") as infile:
        result.append(json.load(infile))

with open("data.json", "wb") as outfile:
     json.dump(result, outfile)
