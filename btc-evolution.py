from datetime import datetime, timedelta
import sys
from Historic_Crypto import HistoricalData

def getBTCevolution(timestamp):
    start = datetime.strptime(timestamp, "%Y-%m-%d-%H-%M")
    end = start + timedelta(hours=24)
    start = start.strftime("%Y-%m-%d-%H-%M")
    end = end.strftime("%Y-%m-%d-%H-%M")
    bitcoin = HistoricalData('BTC-USD',3600,start,end).retrieve_data()
    print((bitcoin.iat[0,3] - bitcoin.iat[24,3])/bitcoin.iat[24,3]*100, "%")

if __name__ == "__main__":
    if (len(sys.argv)==1):
        print("Usage : python btc-evolution.py 2021-11-14-10-00 ")
    else:
        start=sys.argv[1]
        getBTCevolution(start)

    