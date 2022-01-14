from curses.ascii import FF
import sys
from datetime import datetime
from Historic_Crypto import HistoricalData
import numpy as np
from service.client_mongodb import ClientDB
from tqdm import tqdm

class CryptoPrice:
    def __init__(self, currency, start = None, end = None, addToDB = False, update = False):
        if (addToDB):
            self.client_db = ClientDB()
        self.currency = currency

        if (update):
            self.btc_data = self.client_db.get_all(currency + '_data')
            last_data = self.btc_data[len(self.btc_data) - 1]
            self.start = last_data['time'].strftime("%Y-%m-%d-%H-%M")
            self.end = datetime.now().strftime("%Y-%m-%d-%H-%M")
        else:
            self.start = datetime.utcfromtimestamp(start).strftime("%Y-%m-%d-%H-%M")
            self.end = datetime.utcfromtimestamp(end).strftime("%Y-%m-%d-%H-%M")

        self.getDataFrame()
        self.addToDB()

    def getDataFrame(self):
        self.btc_data = HistoricalData(self.currency + "-USD", 900, self.start, self.end).retrieve_data()
        self.btc_data.reset_index(inplace=True)

    def addToDB(self):
        if (self.client_db is not None):
            documents = self.btc_data.to_dict('records')
            for doc in tqdm(documents):
                self.client_db.insert_if_not_in(self.currency + "_data", {'time': doc["time"]}, doc)
            
        else:
            print(self.btc_data.tail())
        

if __name__ == "__main__":
    if (len(sys.argv) == 3 and sys.argv[2] == 'update'):
        getter = CryptoPrice(sys.argv[1], None, None, True, True)
    elif (len(sys.argv) == 5):
        getter = CryptoPrice(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4] == "toDB")
    elif (len(sys.argv) == 4):
        getter = CryptoPrice(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), False)
    else:
        print("Usage 1 (fill a newly created DB) : python crypto_price.py <crypto> <start unix timestamp> <end unix timestamp> <(optional) toDB>")
        print("Usage 2 (update a DB) : python crypto_price.py <crypto> update\n")
        print("Ex 1 : python crypto_price.py BTC 1546297200 1642082712 toDB")
        print("Ex 2 : python crypto_price.py BTC update")

