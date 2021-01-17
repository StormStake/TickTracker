import requests
import json
import time
import asyncio
import aiohttp
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
#get players
async def getCrytpoPlot(ticker, key):
    returnlist = []
    fom = int(time.time() - 2630000*2)
    to = int(time.time())
    urlparams = {
        'symbol':str(ticker),
        'resolution':'D',
        'from':f'{fom}',
        'to':f'{to}',
        'token': key
    }

    async with aiohttp.ClientSession() as session:
        async with session.get('https://finnhub.io/api/v1/crypto/candle', params=urlparams) as resp:
            data = await resp.json()




    return data

async def GetStockPlot(ticker ,key):
    relist = []

    fom = int(time.time() - 2630000*2)
    to = int(time.time())

    urlparams = {
        'symbol':str(ticker),
        'resolution':'D',
        'from':f'{fom}',
        'to':f'{to}',
        'token': key
    }

    async with aiohttp.ClientSession() as session:
        async with session.get('https://finnhub.io/api/v1/stock/candle', params=urlparams) as resp:
            data = await resp.json()
    return data