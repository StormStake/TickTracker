import requests
import json
import time
""" def getpointsbtc():
    with open('data.json', 'r') as f:
                filejson = f.read()
                list = []
                filejson = json.loads(filejson)
                print((len(filejson['bpi'].keys())))
                daycount = 0
                for value in filejson['bpi'].values():
                    list.append((daycount,value/1000))
                    daycount += 1
                return list """

def getCrytpoPlot(ticker, key):
    returnlist = []
    fom = int(time.time() - 31560000)
    to = int(time.time())
    urlparams = {
        'symbol':str(ticker),
        'resolution':'W',
        'from':f'{fom}',
        'to':f'{to}',
        'token': key
    }
    data = json.loads(requests.get('https://finnhub.io/api/v1/crypto/candle', params=urlparams).text)
    timestamps = data['t']
    prices = data['c']
    ymax = max(data['c'])
    ymin = min(data['c'])

    for times, value in zip(range(len(prices)) , prices):
        returnlist.append((times,value))

    return {'plot':returnlist, 'ymax':ymax, 'CurrentPrice': returnlist[-1][1],'ymin': ymin}

def GetStockPlot(ticker ,key):
    relist = []

    fom = int(time.time() - 31560000)
    to = int(time.time())

    urlparams = {
        'symbol':str(ticker),
        'resolution':'W',
        'from':f'{fom}',
        'to':f'{to}',
        'token': key
    }

    data = json.loads(requests.get('https://finnhub.io/api/v1/stock/candle', params=urlparams).text)
    timestamps = data['t']
    prices = data['c']
    ymax = max(data['c'])
    ymin = min(data['c'])
    for times, value in zip(range(len(prices)) , prices):
        relist.append((times,value))

    return {'plot':relist, 'ymax':ymax, 'CurrentPrice': relist[-1][1],'ymin': ymin}