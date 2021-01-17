
url = 'https://finnhub.io/api/v1/stock/candle'
'symbol=AAPL&resolution=1&from=1605543327&to=1605629727&token=bvtss4748v6pijnevmqg'
'symbol=AAPL&resolution=1&from=1610768179&to=1605629727&token=bvtss4748v6pijnevmqg'
urlparams = [
    'symbol=AAPL',
    'resolution=D',
    'from='f'{1610854579-86400}',
    'to='f'{1610854579}',
    'token=''bvtss4748v6pijnevmqg',
]

def urlgener(url, params):
    params='&'.join(params)
    reurl = url + '?' + params
    return reurl
print(urlgener(url, urlparams))