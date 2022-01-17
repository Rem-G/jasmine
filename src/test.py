import pickle
import os
import pandas as pd
import plotly.express as px

def readSave(path, name):
    if name in os.listdir(path):
        with open(f'{path}/{name}', 'rb') as f:
            load = pickle.load(f)
            return load
    else:
        return False

number_of_tweets_by_user = readSave("./src/save", "number_of_tweets_by_user")
df = pd.DataFrame({"name": number_of_tweets_by_user.keys(), "value": number_of_tweets_by_user.values()})
fig = px.bar(df, x = df.name, y = df.value)
fig.show()
