import requests
import json

def getpointsbtc():
    with open('data.json', 'r') as f:
                filejson = f.read()
                list = []
                filejson = json.loads(filejson)
                print((len(filejson['bpi'].keys())))
                daycount = 0
                for value in filejson['bpi'].values():
                    list.append((daycount,value/1000))
                    daycount += 1
                return list


def GetStockPlot(ticker ,key):
    relist = []
    import time
    fom = int(time.time() - 31560000)
    to = int(time.time())

    urlparams = {
        'symbol':str(ticker),
        'resolution':'W',
        'from':f'{1578822759}',
        'to':f'{1610382761}',
        'token': key
    }

    data = json.loads(requests.get('https://finnhub.io/api/v1/stock/candle', params=urlparams).text)

    timestamps = data['t']
    prices = data['c']
    ymax = max(data['c'])

    for times, value in zip(range(len(prices)) , prices):
        relist.append((times,value))

    return {'plot':relist, 'ymax':ymax, 'CurrentPrice': relist[-1][1]}