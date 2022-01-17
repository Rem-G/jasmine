from operator import mod
import os
import pickle
from sys import path
from traceback import print_tb
from unicodedata import name
from xmlrpc.client import DateTime
from sentiment_analysis import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from transformers import pipeline
import time
import numpy as np

class Sentiment:
    def __init__(self, model_nb, model_transformers, model_sentiment_intensiry) -> None:
        self.classifer_naive_bayes = model_nb
        self.classifier_transformers = model_transformers
        self.classifer_sentiment_intensity = model_sentiment_intensiry

    def classify_sentiment_intensity_analyzer(self, texts):
        pos, neg, neu = 0, 0, 0
        for text in texts:
            pos += self.classifer_sentiment_intensity.polarity_scores(text)['pos']
            neg += self.classifer_sentiment_intensity.polarity_scores(text)['neg']
            neu += self.classifer_sentiment_intensity.polarity_scores(text)['neu']
        return (neg + (neu/2))/len(texts), (pos + (neu/2))/len(texts)

    def classify_transformers(self, texts):
        text = " ".join(texts)
        result = self.classifier_transformers(text)[0]
        if result["label"] == "POSITIVE":
            return 1- result["score"], result["score"]
        return result["score"], 1- result["score"]

    def clissify_naive_bayes(self, texts):
        neg, pos = [], []
        for text in texts :
            val = classify_naive_bayes(text, self.classifer_naive_bayes)
            neg.append(val[0])
            pos.append(val[1])
        return np.mean(neg), np.mean(pos)

    def get_all_mean(self, texts):
        s1 = self.classify_sentiment_intensity_analyzer(texts)
        s2 = self.classify_transformers(texts)
        s3 = self.clissify_naive_bayes(texts)
        return {"neg" : (s1[0] + s2[0] + s3[0])/3, "pos": (s1[1] + s2[1] + s3[1])/3}

def readSave(path, name):
    if name in os.listdir(path):
        with open(f'{path}/{name}', 'rb') as f:
            load = pickle.load(f)
            return load
    else:
        return False

if __name__ == "__main__":
    model = readSave("./src/model", "classifer_sentiment")
    classifier_transformers = pipeline('sentiment-analysis')
    classifer_sentiment_intensity = SentimentIntensityAnalyzer()
    texts = ["I want to kill you", "I like murder"]
    start_time = time.time()
    print(Sentiment(model, classifier_transformers, classifer_sentiment_intensity).get_all_mean(texts))
    print(time.time() - start_time)
