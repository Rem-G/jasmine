from operator import mod
import os
import pickle
from sys import path
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
        leng = 0
        pos, neg, neu = 0
        for text in texts:
            leng += 1
            pos += self.classifer_sentiment_intensity.polarity_scores(text)['pos']
            neg += self.classifer_sentiment_intensity.polarity_scores(text)['neg']
            neu += self.classifer_sentiment_intensity.polarity_scores(text)['neu']
        return (neg + (neu/2))/leng, (pos + (neu/2))/leng

    def classify_transformers(self, text):
        result = self.classifier_transformers(text)[0]
        if result["label"] == "POSITIVE":
            return 1- result["score"], result["score"]
        return result["score"], 1- result["score"]

    def clissify_naive_bayes(self, texts):
        return np.mean([classify_naive_bayes(text, self.classifer_naive_bayes) for text in texts])

    def get_all(self, text):
        s1 = self.classify_sentiment_intensity_analyzer(text)
        s2 = self.classify_transformers(text)
        s3 = self.clissify_naive_bayes(text)
        return {"si_neg": s1[0], "si_pos": s1[1], "tf_neg": s2[0], "tf_pos": s2[1], "nb_neg": s3[0], "nb_pos": s3[1]}

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
    text = "TESLA ACCEPTING #DOGECOIN IS HUGE!!!!!! Thank you Elon! We are live right now on YouTube covering this:"
    start_time = time.time()
    print(Sentiment(model, classifier_transformers, classifer_sentiment_intensity, text).get_all())
    print(Sentiment(model, classifier_transformers, classifer_sentiment_intensity, text).get_all())
    print(Sentiment(model, classifier_transformers, classifer_sentiment_intensity, text).get_all())
    print(Sentiment(model, classifier_transformers, classifer_sentiment_intensity, text).get_all())
    print(Sentiment(model, classifier_transformers, classifer_sentiment_intensity, text).get_all())
    print(Sentiment(model, classifier_transformers, classifer_sentiment_intensity, text).get_all())
    print(Sentiment(model, classifier_transformers, classifer_sentiment_intensity, text).get_all())
    print(Sentiment(model, classifier_transformers, classifer_sentiment_intensity, text).get_all())
    print(Sentiment(model, classifier_transformers, classifer_sentiment_intensity, text).get_all())
    print(Sentiment(model, classifier_transformers, classifer_sentiment_intensity, text).get_all())
    print(Sentiment(model, classifier_transformers, classifer_sentiment_intensity, text).get_all())
    print(Sentiment(model, classifier_transformers, classifer_sentiment_intensity, text).get_all())
    print(Sentiment(model, classifier_transformers, classifer_sentiment_intensity, text).get_all())
    print(Sentiment(model, classifier_transformers, classifer_sentiment_intensity, text).get_all())
    print(Sentiment(model, classifier_transformers, classifer_sentiment_intensity, text).get_all())
    print(Sentiment(model, classifier_transformers, classifer_sentiment_intensity, text).get_all())
    print(Sentiment(model, classifier_transformers, classifer_sentiment_intensity, text).get_all())
    print(Sentiment(model, classifier_transformers, classifer_sentiment_intensity, text).get_all())
    print(Sentiment(model, classifier_transformers, classifer_sentiment_intensity, text).get_all())
    print(Sentiment(model, classifier_transformers, classifer_sentiment_intensity, text).get_all())
    print(Sentiment(model, classifier_transformers, classifer_sentiment_intensity, text).get_all())
    print(Sentiment(model, classifier_transformers, classifer_sentiment_intensity, text).get_all())
    print(Sentiment(model, classifier_transformers, classifer_sentiment_intensity, text).get_all())
    print(Sentiment(model, classifier_transformers, classifer_sentiment_intensity, text).get_all())
    print(time.time() - start_time)
