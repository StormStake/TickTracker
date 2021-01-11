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
def getpointsstock(ticker):
    relist = []
    import time
    urlparams = {
        
        'symbol':'IBM',
        'resolution':'W',
        'from':f'{int(time.time() - 31500000)}',
        'to':f'{int(time.time()-60)}',
        'token':'sandbox_bvtstjn48v6pijnevq2g'
    }
    data = json.loads(requests.get('https://finnhub.io/api/v1/stock/candle', params=urlparams).text)
    #with open('api.json') as f:
    #    data = json.loads(f.read())
    #Useful?
    timestamps = data['t']
    prices = data['c']
    ymax = max(data['c'])

    for times, value in zip(range(55) , prices):
        relist.append((times,value))
    
    return {'plot':relist, 'ymax':ymax}