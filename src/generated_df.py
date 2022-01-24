from service.client_mongodb import ClientDB
import pandas as pd
import pickle
import pickle
from sentiment_analysis import *
from datetime import datetime
from tqdm import tqdm

ClientDB = ClientDB()
lt = datetime(2022,1,22,20, 00, 00)
gte = datetime(2019,1,1,0,0)
key_words = ["Bitcoin", "Btc", "₿", "#Bitcoin", "#Btc", "#₿", "$btc", "crypto", "Satoshi", "fed", "#crypto", "#Satoshi", "#fed", "cryptocurrency", "#cryptocurrency"]
df = pd.DataFrame()
get_tweets = ClientDB.between_date('tweets', "created_at", lt=lt, gte=gte)
for i in tqdm(get_tweets):
    if any(keyw.upper() in i["text"].upper() for keyw in key_words):
        df = df.append(pd.Series(i), ignore_index=True)

print("Save tweets with pickle")
with open("./src/data/df.pickle", 'wb') as f:
    pickle.dump(df, f)