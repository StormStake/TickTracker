import requests
import json
import time
import threading

class helper():
    def __init__(self):
        self.publicdata = []
        self.cryptos = []
        self.data = {}
        self.listoftargets = []
        for dicto in json.loads(requests.get('https://finnhub.io/api/v1/crypto/symbol?exchange=binance&token=bvtss4748v6pijnevmqg').text):
            self.cryptos.append(dicto['symbol'])
        self.dt = 0


    def addtotargets(self, ticker):
        if ticker not in self.listoftargets:
            self.listoftargets.append(ticker)
        else:
            return(False)


    def threadingtarget(self):
        def thing():
            self.obatinresults(self.listoftargets, 'bvtss4748v6pijnevmqg')
        threading.Timer(1/30, thing).start()


    def getdata(self, ticker):
        try:
            return self.data[ticker]
        except:
            return 0

    def start(self):

        x = threading.Thread(target=self.threadingtarget)
        x.start()




    def obatinresults(self, tickers, key):

        for ticker in tickers:
            if ticker in self.cryptos:

                self.data[ticker] = self.getCrytpoPlot(ticker, key)
            else:
                self.data[ticker] = self.getStockPlot(ticker, key)




    def getStockPlot(self, ticker ,key):


        relist = []

        fom = int(time.time() - 31560000)
        to = int(time.time()-30)

        urlparams = {
            'symbol':str(ticker),
            'resolution':'D',
            'from':f'{fom}',
            'to':f'{to}',
            'token': key
        }

        data = json.loads(requests.get('https://finnhub.io/api/v1/stock/candle', params=urlparams).text)
        try:
            timestamps = data['t']
            prices = data['c']
            ymax = max(data['c'])
            ymin = min(data['c'])
            for times, value in zip(range(len(prices)) , prices):
                relist.append((times,value))
            return {'plot':relist, 'ymax':ymax, 'CurrentPrice': relist[-1][1],'ymin': ymin, 'ticker':ticker}
        except KeyError:
            return {'CurrentPrice': 0}


    def getCrytpoPlot(self, ticker, key):
        returnlist = []
        fom = int(time.time() - 31560000)
        to = int(time.time()-30)
        urlparams = {
            'symbol':str(ticker),
            'resolution':'D',
            'from':f'{fom}',
            'to':f'{to}',
            'token': key
        }
        data = json.loads(requests.get('https://finnhub.io/api/v1/crypto/candle', params=urlparams).text)
        try:
            print(data)
            timestamps = data['t']
            prices = data['c']
            ymax = max(data['c'])
            ymin = min(data['c'])

            for times, value in zip(range(len(prices)) , prices):
                returnlist.append((times,value))
            return {'plot':returnlist, 'ymax':ymax, 'CurrentPrice': returnlist[-1][1],'ymin': ymin, 'ticker':ticker}
        except KeyError:
            return {'CurrentPrice': 0}
