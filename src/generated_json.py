import json
from service.client_mongodb import ClientDB
from datetime import datetime

ClientDB = ClientDB()
TableDB = "tweets"
key_words = ["Bitcoin", "Btc", "₿", "#Bitcoin", "#Btc", "#₿", "$btc", "crypto", "Satoshi", "fed", "#crypto", "#Satoshi", "#fed", "cryptocurrency", "#cryptocurrency"]

date_start_bear = [datetime(2021,5,6), datetime(2021,11,9), datetime(2020,3,10), datetime(2021,1,14)]
date_end_bear = [datetime(2021,5,19), datetime(2022,1,20), datetime(2020,3,13), datetime(2021,1,27)]

date_start_bull = [datetime(2021,9,21), datetime(2021,7,13), datetime(2021,1,25), datetime(2020,9,20)]
date_end_bull = [datetime(2021,10,20), datetime(2021,7,30),  datetime(2021,1,20), datetime(2021,1,8)]

bear = []
pull = []
for i in range(len(date_start_bear)):
    for tweet in ClientDB.between_date(TableDB, "created_at", date_start_bear[i], date_end_bear[i]):
        if any(keyw.upper() in tweet["text"].upper() for keyw in key_words):
            bear.append({"text": tweet["text"]})

for i in range(len(date_start_bull)):
    for tweet in ClientDB.between_date(TableDB, "created_at", date_start_bull[i], date_end_bull[i]):
        if any(keyw.upper() in tweet["text"].upper() for keyw in key_words):
            pull.append({"text": tweet["text"]})

with open("./src/data/beer.json", "w") as f:
    json.dump(bear, f)

with open("./src/data/bull.json", "w") as f:
    json.dump(pull, f)


