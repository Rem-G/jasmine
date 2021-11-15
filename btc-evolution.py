from datetime import datetime, timedelta
from Historic_Crypto import HistoricalData

sampleStart = '2021-11-14-16-00'

def getBTCevolution(timestamp):
    start = datetime.strptime(timestamp, "%Y-%m-%d-%H-%M")
    end = start + timedelta(hours=24)
    start = start.strftime("%Y-%m-%d-%H-%M")
    end = end.strftime("%Y-%m-%d-%H-%M")
    bitcoin = HistoricalData('BTC-USD',3600,start,end).retrieve_data()
    print((bitcoin.iat[0,3] - bitcoin.iat[23,3])/bitcoin.iat[23,3]*100, "%")

if __name__ == "__main__":
    getBTCevolution(sampleStart)