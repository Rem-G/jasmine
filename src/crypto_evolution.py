import sys
from datetime import datetime
import time
import numpy as np
from service.client_mongodb import ClientDB

btc_col = 'BTC_data'
tweets_col = 'tweets'

class CryptoEvolution:
    def __init__(self, evolution_period):
        self.client_db = ClientDB()
        self.btc_documents = self.client_db.get_all(btc_col)
        self.tweets_documents = self.client_db.get_all(tweets_col)
        self.evolution_period = evolution_period

        self.addEvolution()
        self.addToDB()
        

    def addEvolution(self):
        for tweet in self.tweets_documents:
            unix_timestamp  = time.mktime(tweet["created_at"].timetuple())
            floored_unix_timestamp = unix_timestamp - (unix_timestamp % 900)

            ts = self.dtFromUnix(floored_unix_timestamp)
            
            ts_index = None
            for i in range(len(self.btc_documents)):
                if (self.btc_documents[i]['time'] == ts):
                    ts_index = i

            before_index = ts_index - 4 * self.evolution_period
            after_index = ts_index + 4 * self.evolution_period

            if (ts_index is not None and before_index > 0 and after_index < len(self.btc_documents)):
                before_price_ev = (self.btc_documents[ts_index]['close'] - self.btc_documents[before_index]['close']) / self.btc_documents[before_index]['close']
                after_price_ev = (self.btc_documents[after_index]['close'] - self.btc_documents[ts_index]['close']) / self.btc_documents[ts_index]['close']

                tweet["evolution_before"] = before_price_ev
                tweet["evolution_after"] = after_price_ev

                tweet["log_diff_before"] = np.log(self.btc_documents[ts_index]['close']) - np.log(self.btc_documents[before_index]['close'])
                tweet["log_diff_before"] = np.log(self.btc_documents[after_index]['close']) - np.log(self.btc_documents[ts_index]['close'])

                b_vol=0
                a_vol=0
                for i in range(4 * self.evolution_period):
                    b_vol = b_vol + self.btc_documents[ts_index - i]['volume']
                    a_vol = a_vol + self.btc_documents[ts_index + (i + 1)]['volume']
                tweet["volume_before"] = b_vol
                tweet["volume_after"] = a_vol
            else:
                tweet["evolution_before"] = None
                tweet["evolution_after"] = None
                tweet["log_diff_before"] = None
                tweet["log_diff_before"] = None
                tweet["volume_before"] = None
                tweet["volume_after"] = None


    def addToDB(self):
        for doc in self.tweets_documents:
            self.client_db.update_document(tweets_col, {'created_at': doc["created_at"]}, doc)

    def dtFromUnix(unix):
        return datetime.utcfromtimestamp(unix)
        

if __name__ == "__main__":
    if (len(sys.argv) == 2):
        ce = CryptoEvolution(int(sys.argv[1]))
    else:
        print("Usage : python crypto_evolution.py <evolution period (hours)>\n")
        print("Ex : python crypto_evolution.py 24")

