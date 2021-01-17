import requests
import json
import time
import threading
import datetime


class helper():
    def __init__(self):
        self.publicdata = []
        self.cryptos = []
        self.data = {}
        self.listoftargets = []
        for dicto in json.loads(requests.get('https://finnhub.io/api/v1/crypto/symbol?exchange=binance&token=bvtss4748v6pijnevmqg').text):
            self.cryptos.append(dicto['symbol'])
        self.resolutions = [1, 5, 15, 30, 60, 'D', 'W', 'M']
        self.resolution = 30
        self.targetResolution = 0


        self.targets = ['W','M','Y','YTD']
        self.timeSpans = {'Y': 31536000, 'YTD':datetime.datetime(datetime.date.today().year,1,1,0,0).timestamp(), 'M': 2628000, 'W':604800,}
        self.timeSpanTarget = 0
    #Public Methods
    def changeTimeSpan(self, span):
        self.timeSpan = self.timeSpans[span]

    def nextTimeSpan(self):
        self.timeSpanTarget += 1

        if self.timeSpanTarget == 4:
            self.timeSpanTarget = 0

        self.timeSpan = self.timeSpans[self.targets[self.timeSpanTarget]]

    def ChangeResolution(self, rez):
        self.targetResolution = self.resolutions.index(rez)
        self.resolution = self.targetResolution

    def getTimeSpan(self):
        return self.targets[self.timeSpanTarget]

    def addtotargets(self, ticker):
        if ticker not in self.listoftargets:
            self.listoftargets.append(ticker)
        else:
            return(False)

    def nextResolution(self):
        self.targetResolution += 1
        if self.targetResolution == 8:
            self.targetResolution = 0
        self.ChangeResolution(self.resolutions[self.targetResolution])

    #public methods end

    #level one data collection
    def getdata(self, ticker):

        try:
            return self.data[ticker]

        except:
            return {'Fail': True}

    #starts the data refreshing
    def start(self, *dt):

        x = threading.Thread(target=self.obatinresults,args=[self.listoftargets, 'bvtss4748v6pijnevmqg'])
        x.start()




    #level two api
    def obatinresults(self, tickers, key):

        for ticker in tickers:

            if ticker in self.cryptos:
                self.data[ticker] = self.getCrytpoPlot(ticker, key)

            else:
                self.data[ticker] = self.getStockPlot(ticker, key)


    #level one api
    def getStockPlot(self, ticker ,key):

        plot = []

        starttime = int(time.time() - self.timeSpan)
        endtime = int(time.time())

        urlparams = {
            'symbol':str(ticker),
            'resolution':self.resolution,
            'from':f'{starttime}',
            'to':f'{endtime}',
            'token': key
        }
        before = time.time()
        data = json.loads(requests.get('https://finnhub.io/api/v1/stock/candle', params=urlparams).text)
        print(f'request took {before - time.time()} seconds')
        try:
            timestamps = data['t']
            prices = data['c']
            ymax = max(data['c'])
            ymin = min(data['c'])
            for times, value in zip(range(len(prices)) , prices):
                plot.append((times,value))
            return {'plot':plot, 'ymax':ymax, 'CurrentPrice': prices[-1],'ymin': ymin, 'ticker':ticker, 'Fail': False}

        except KeyError:
            return {'Fail': True}

    #level one api
    def getCrytpoPlot(self, ticker, key):

        plot = []
        
        starttime = int(time.time() - self.timeSpan)
        endtime = int(time.time())
        urlparams = {
            'symbol':str(ticker),
            'resolution':self.resolution,
            'from':f'{starttime}',
            'to':f'{endtime}',
            'token': key
        }

        before = time.time()
        data = json.loads(requests.get('https://finnhub.io/api/v1/crypto/candle', params=urlparams).text)
        print(f'request took {before - time.time()} seconds')
        try:
            timestamps = data['t']
            prices = data['c']
            ymax = max(data['c'])
            ymin = min(data['c'])

            for times, value in zip(range(len(prices)) , prices):
                plot.append((times,value))
            return {'plot':plot, 'ymax':ymax, 'CurrentPrice': prices[-1],'ymin': ymin, 'ticker':ticker,'Fail': False}

        except:
            return {'Fail': True}
