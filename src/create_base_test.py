from traceback import print_tb
from service.client_mongodb import ClientDB
import pandas as pd
import pickle
import os
import pickle
from sentiment_analysis import *
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
# from transformers import pipeline
# from compute_sentiment import Sentiment
from datetime import datetime
# Variable
ClientDB = ClientDB()
TableDB = "tweets_test_1an"

lte = datetime(2021,12,31)
gte = datetime(2021, 1, 1)
key_words = ["Bitcoin", "Btc", "₿", "#Bitcoin", "#Btc", "#₿", "$btc"]
get_tweets = ClientDB.between_date('tweets', "created_at", lt=lte, gte=gte)
index = 1
for i in get_tweets:
    if any(keyw.upper() in i["text"].upper() for keyw in key_words):
        ClientDB.import_document(TableDB, i)
        print(f"Imporation terminée : {index}")
        index += 1

# df = pd.DataFrame()
# get_tw = ClientDB.get_all(TableDB)

# for tw in get_tw:
#     t = pd.Series(tw)
#     df = df.append(t, ignore_index=True)



# with open("./src/save/df_twitts_test", 'wb') as f:
#     pickle.dump(df, f)

# with open(f'./src/save/df_twitts_test', 'rb') as f:
#     df = pickle.load(f)
# def readSave(path, name):
#     if name in os.listdir(path):
#         with open(f'{path}/{name}', 'rb') as f:
#             load = pickle.load(f)
#             return load
#     else:
#         return False
# model = readSave("./src/model", "classifer_sentiment")
# classifier_transformers = pipeline('sentiment-analysis')
# classifer_sentiment_intensity = SentimentIntensityAnalyzer()
# def l(x):
#     print("Processing")
#     print(x)
#     return 
    

# df['sentiment'] = df['text'].apply(lambda x : Sentiment(model, classifier_transformers, classifer_sentiment_intensity, x).get_all())

# print(df)
# with open(f'./src/save/df_twitts_test_end', 'wb') as f:
#     df = pickle.dump(df, f)

# ["si_neg", "si_neu", "si_pos", "tf_neg", "tf_pos", "nb_neg", "nb_pos"]
# with open(f'./src/save/df_twitts_test_end', 'rb') as f:
#     df = pickle.load(f)
# print(df)
# df["si_neg"] = None
# df["si_neu"] = None
# df["si_pos"]= None
# df["tf_neg"]= None
# df["tf_pos"]= None
# df["nb_neg"]= None
# df["nb_pos"]= None
# for i in df.index:
#     val = df["sentiment"][i]
#     df["si_neg"][i] = val["si_neg"]
#     df["si_neu"][i] = val["si_neu"]
#     df["si_pos"][i] = val["si_pos"]
#     df["tf_neg"][i] = val["tf_neg"]
#     df["tf_pos"][i] = val["tf_pos"]
#     df["nb_neg"][i] = val["nb_neg"]
#     df["nb_pos"][i] = val["nb_pos"]

# with open(f'./src/save/df_twitts_test_bis', 'wb') as f:
#     df = pickle.dump(df, f)

# with open('./src/save/df_twitts_test_bis', 'rb') as f:
#   df = pickle.load(f)
# print(df)