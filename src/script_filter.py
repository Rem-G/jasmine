from service.client_mongodb import ClientDB
Table_tweet = "tweets"
Table_account = "influent_bitcoin_account"
ClientDB = ClientDB()
import datetime
from datetime import date, datetime, timedelta
import matplotlib.pyplot as plt
from crypto_evolution import getCryptoEvolution
import plotly.express as px
import pandas as pd
import pickle

def getDateRange(start, end, delta):
    list_of_date = []
    list_of_date.append(start)
    new_date = start + timedelta(minutes=delta)
    while new_date < end:
        list_of_date.append(new_date) 
        new_date = new_date + timedelta(minutes=delta)
    return list_of_date


if __name__ == "__main__":
    start, end = datetime(2021, 10, 10), datetime(2022, 1, 10)
    delta = 240
    date_range = getDateRange(start, end, delta)
    KEYWORD = ["Bitcoin", "Btc", "₿", "Crypto", "#Bitcoin", "#Btc", "#₿", "#Crypto"]
    rt_date = {}
    cours_date = {}

    for i in range(len(date_range) - 2):
        list = ClientDB.between_date(Table_tweet,"created_at", date_range[i], date_range[i + 1])
        date = date_range[i]
        date1 = (date.strftime("%Y-%m-%d-%H-%M"))
        rt_date[date] = 0
        cours_date[date] = getCryptoEvolution('BTC-USD', date1, 4)
        for j in list:
            if any(keyw.upper() in j['text'].upper() for keyw in KEYWORD):
                rt_date[date] += j['retweet_count']

    x = rt_date.keys()
    y = rt_date.values()
    x1 = cours_date.keys()
    y1 = cours_date.values()
    df = pd.DataFrame({"date": x, "rt": y, "btc-evol": y1})
    with open("./src/save/df", 'wb') as f:
        pickle.dump(df, f)
    fig = px.line(df)
    fig.show()