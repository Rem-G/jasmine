import sys
from datetime import datetime
from Historic_Crypto import HistoricalData
import numpy as np
from service.client_mongodb import ClientDB

class CryptoPrice:
    def __init__(self, currency, start, end, addToDB = False):
        if (addToDB):
            self.client_db = ClientDB()
        self.currency = currency
        self.start = datetime.utcfromtimestamp(start).strftime("%Y-%m-%d-%H-%M")
        self.end = datetime.utcfromtimestamp(end).strftime("%Y-%m-%d-%H-%M")

        self.getDataFrame()
        self.addDFToDB()

    def getDataFrame(self):
        self.btc_data = HistoricalData(self.currency + "-USD", 900, self.start, self.end).retrieve_data()
        self.btc_data.reset_index(inplace=True)

    def addDFToDB(self):
        if (self.client_db is not None):
            documents = self.btc_data.to_dict('records')
            for doc in documents:
                self.client_db.insert_if_not_in(self.currency + "_data", {'time': doc["time"]}, doc)
            
        else:
            print(self.btc_data.tail())
        

if __name__ == "__main__":
    if (len(sys.argv) == 5):
        getter = CryptoPrice(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4] == "toDB")
    elif (len(sys.argv) == 4):
        getter = CryptoPrice(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), False)
    else:
        print("Usage : python crypto_price.py <crypto> <start unix timestamp> <end unix timestamp> <(optional) toDB>\n")
        print("Ex : python crypto_price.py BTC 1546297200 1642082712 toDB")

