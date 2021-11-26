from datetime import datetime, timedelta
import sys
from Historic_Crypto import HistoricalData

def getCryptoEvolution(timestamp):
    start = datetime.strptime(timestamp, "%Y-%m-%d-%H-%M")
    end = start + timedelta(hours=period)
    start = start.strftime("%Y-%m-%d-%H-%M")
    end = end.strftime("%Y-%m-%d-%H-%M")
    price = HistoricalData('BTC-USD',3600,start,end).retrieve_data()
    print((price.iat[0,3] - price.iat[period,3])/price.iat[period,3]*100, "%")

if __name__ == "__main__":
    print(len(sys.argv))
    if (len(sys.argv)<3):
        print("Usage : python crypto_evolution.py <crypto> <start timestamp> <period(hours)=24>\n")
        print("Ex : python crypto_evolution.py BTC 2021-11-14-10-00 24")
    elif (len(sys.argv)==3):
        crypto = sys.argv[1]
        timestamp = sys.argv[2]
        period = 24
        getCryptoEvolution(timestamp)
    else:
        crypto = sys.argv[1]
        timestamp = sys.argv[2]
        period = int(sys.argv[3])
        getCryptoEvolution(timestamp)

    