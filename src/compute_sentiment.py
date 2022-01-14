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


class Sentiment:
    def __init__(self, model_nb, model_transformers, model_sentiment_intensiry, text) -> None:
        self.text = text
        self.classifer_naive_bayes = model_nb
        self.classifier_transformers = model_transformers
        self.classifer_sentiment_intensity = model_sentiment_intensiry

    def classify_sentiment_intensity_analyzer(self):
        return self.classifer_sentiment_intensity.polarity_scores(self.text)['neg'], self.classifer_sentiment_intensity.polarity_scores(self.text)['neu'], self.classifer_sentiment_intensity.polarity_scores(self.text)['pos']

    def classify_transformers(self):
        result = self.classifier_transformers(self.text)[0]
        if result["label"] == "POSITIVE":
            return 1- result["score"], result["score"]
        return result["score"], 1- result["score"]

    def clissify_naive_bayes(self):
        return classify_naive_bayes(self.text, self.classifer_naive_bayes)

    def get_all(self):
        s1 = self.classify_sentiment_intensity_analyzer()
        s2 = self.classify_transformers()
        s3 = self.clissify_naive_bayes()
        return {"si_neg": s1[0], "si_neu": s1[1], "si_pos": s1[2], "tf_neg": s2[0], "tf_pos": s2[1], "nb_neg": s3[0], "nb_pos": s3[1]}


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
