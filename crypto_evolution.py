import sys
from datetime import datetime, timedelta
from Historic_Crypto import HistoricalData

def getCryptoEvolution(crypto, timestamp, period):
    start = datetime.strptime(timestamp, "%Y-%m-%d-%H-%M")
    end = start + timedelta(hours=period)

    avgVolume = getAvgVolume(crypto, timestamp, period, start)

    start = start.strftime("%Y-%m-%d-%H-%M")
    end = end.strftime("%Y-%m-%d-%H-%M")
    price = HistoricalData(crypto,900,start,end).retrieve_data()

    vol=0
    for i in range(len(price)):
        vol = vol + price.iat[i,4]

    priceEv = (price.iat[len(price)-1,3] - price.iat[0,3]) / price.iat[0,3] * 100
    volEv = (vol - avgVolume) / avgVolume * 100

    print("\n")
    print(start, ":", price.iat[0,3], "$")
    print(end, ":", price.iat[len(price)-1,3], "$")
    print(period, "hours evolution :", priceEv, "%")
    print("\n")
    print(period, "hours Volume :", vol)
    print("30 days AVG", period, "hours Volume :", avgVolume)
    print("Volume evolution :", volEv, "%")


def getAvgVolume(crypto, timestamp, period, start):
    end = start
    start = start - timedelta(days=30)
    start = start.strftime("%Y-%m-%d-%H-%M")
    end = end.strftime("%Y-%m-%d-%H-%M")

    data = HistoricalData(crypto,86400,start,end).retrieve_data()

    vol=0
    for i in range(len(data)):
        vol = vol + data.iat[i,4]
    
    return vol/30*period/24


if __name__ == "__main__":
    if (len(sys.argv)<3):
        print("Usage : python crypto_evolution.py <crypto> <start timestamp> <period(hours)=24>\n")
        print("Ex : python crypto_evolution.py BTC 2021-11-14-10-00 24")
    elif (len(sys.argv)==3):
        crypto = sys.argv[1] + '-USD'
        timestamp = sys.argv[2]
        period = 24
        getCryptoEvolution(crypto, timestamp, period)
    else:
        crypto = sys.argv[1] + '-USD'
        timestamp = sys.argv[2]
        period = int(sys.argv[3])
        getCryptoEvolution(crypto, timestamp, period)

    