import json
import re
import string

import nltk
from nltk import FreqDist
from nltk.corpus import stopwords, twitter_samples
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk import classify
from nltk import NaiveBayesClassifier
from nltk.tokenize import word_tokenize

import pickle
import random

import os

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

if __name__ == "__main__":
    stop_words = stopwords.words('english')
    with open("./src/data/beer.json", 'r') as f:
        beer_tweets = json.load(f)
    with open("./src/data/bull.json", 'r') as f:
        bull_tweets = json.load(f)

    bull_tweet_tokens = [nltk.sent_tokenize(tweet['text']) for tweet in bull_tweets]
    beer_tweet_tokens = [nltk.sent_tokenize(tweet['text']) for tweet in beer_tweets]

    positive_cleaned_tokens_list = []
    negative_cleaned_tokens_list = []
    for tokens in bull_tweet_tokens:
        positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))
    for tokens in beer_tweet_tokens:
        negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))


    def get_tweets_for_model(cleaned_tokens_list):
        for tweet_tokens in cleaned_tokens_list:
            yield dict([token, True] for token in tweet_tokens)

    positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
    negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)


    positive_dataset = [(tweet_dict, "Beer")
                        for tweet_dict in positive_tokens_for_model]

    negative_dataset = [(tweet_dict, "Bull")
                        for tweet_dict in negative_tokens_for_model]

    dataset = positive_dataset + negative_dataset

    random.shuffle(dataset)
    classifier = NaiveBayesClassifier.train(dataset)

    with open("./src/model/classifer_bull_bear", "wb") as write:
        pickle.dump(classifier, write)

def classify_bull_bear(text, model):
    custom_tokens = remove_noise(word_tokenize(text))
    estimation = model.prob_classify(dict([token, True] for token in custom_tokens))
    return estimation.prob("Beer"), estimation.prob("Bull")