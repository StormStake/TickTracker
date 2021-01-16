from kivy.uix.boxlayout import BoxLayout

from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy_garden.graph import Graph, SmoothLinePlot
from kivy.core.window import Window
from kivy.lang import Builder
import jsonhelper
import requests
import json
import time
from functools import partial
import asyncio
import aiohttp
Builder.load_string("""
<MyImage>:
    bcolor: 0, 0, 0, 1
    canvas.before:
        Color:
            rgba: root.bcolor
        Rectangle:
            size: self.size
            pos: self.pos
""")

Builder.load_string("""
<MyBox>:
    bcolor: 0, 0, 0, 1
    canvas.before:
        Color:
            rgba: root.bcolor
        Rectangle:
            size: self.size
            pos: self.pos
""")

class MyBox(BoxLayout):
    pass
class MyImage(Image):
    pass

class Myapp(App):

    #App Entry Point
    def build(self):


        #for fullscreen use
        Window.fullscreen = 'auto'

        #for window use
        #Window.borderless = '0'
        #Window.size = (1920,1080)
        #Window.clearcolor = (0.1,0.1,0.1,1)
        #layout setup

        pageslay = PageLayout(border="20")

        Page1 = GraphPage('IBM')
        Page2 = GraphPage('AAPL')
        Page3 = GraphPage('BINANCE:BTCUSDT')

        pages = [Page1, Page2, Page3]
        pageslay.add_widget(Page1.getWidget())
        pageslay.add_widget(Page2.getWidget())
        pageslay.add_widget(Page3.getWidget())


        def update(rap):
            gjruihfdhusi = []
            for page in pages:
                gjruihfdhusi.append( asyncio.run(page.getchart().get_point_data()))
            #print(gjruihfdhusi)[1]


        #for some reason i couldn't get a classes method to run in schedule_interval
        Clock.schedule_interval(update, 1/30)
        return pageslay


class GraphPage():
    def __init__(self, ticker):

        self.chart = linechart(ticker)

        self.Page = MyBox(orientation="vertical")

        #Upper Layout
        upperLayout = MyBox(orientation="horizontal")
        upperLayout.add_widget(Label(text=f'Current Quote:\n {str(round(self.chart.CurrentPrice, 2))}', font_size='35sp'))


        try:
            upperLayout.add_widget(MyImage(source=f"{''.join(ticker.split(':'))}.png"))
        except:
            upperLayout.add_widget(MyImage(source=f'NA.png'))
        #Lower Layout
        self.Page.add_widget(upperLayout)
        self.Page.add_widget(self.chart.Get_graph())

    def getWidget(self):
        return self.Page

    def getchart(self):
        return self.chart

class linechart():
    def __init__(self, ticker):
        self.CurrentPrice = 0
        self.dt = 0
        self.ticker = ticker
        self.cryptos = []
        self.yticks = 100
        for dicto in json.loads(requests.get('https://finnhub.io/api/v1/crypto/symbol?exchange=binance&token=bvtss4748v6pijnevmqg').text):

            self.cryptos.append(dicto['symbol'])


        self.xticks = 10
        self.xmax = 50
        self.chart = Graph(
            xlabel='Time',
            ylabel='Price',
            x_ticks_minor=0,
            x_ticks_major=self.xticks,
            y_ticks_major=self.yticks,
            y_grid_label=True,
            x_grid_label=True,
            padding=5,
            x_grid=True,
            y_grid=True,
            xmin=0,
            xmax=self.xmax,
            ymin=0,
            )


        self.plot = SmoothLinePlot(color=[1, 1, 1, 1])
        self.chart.add_plot(self.plot)




    #main
    def get_point_data(self):
        if self.dt+5 < time.time():
            data = self.getPointsFromApi()
            
            self.dt = time.time()
            self.data_handle(data)


    def data_handle(self, data):
        if data is None:
            return
        timestamps = data['t']
        prices = data['c']
        plot = []
        ymax = max(data['c'])
        ymin = min(data['c'])
        for times, value in zip(range(len(prices)) , prices):
            plot.append((times,value))

        self.plot.points = plot

        self.CurrentPrice = data['c'][-1]
        self.yticks = (self.chart.ymax - self.chart.ymin)/4
        self.chart.y_ticks_major = self.yticks
        self.plot.points = plot
        self.xmax = len(self.plot.points)-1
        self.chart.xmax = self.xmax

        #sizing graph adding upper buffer
        self.chart.ymax = round((ymax+ymax/4)/10)*10
        self.chart.ymin = round((ymin-ymin/4)/10)*10
        #sizing xmax
        self.xmax = len(plot)




    def getPointsFromApi(self, *dt):
        if self.ticker in self.cryptos:
            data = jsonhelper.getCrytpoPlot(self.ticker, 'bvtss4748v6pijnevmqg')
        else:
            data = jsonhelper.GetStockPlot(self.ticker, 'bvtss4748v6pijnevmqg')
        return data



    def Get_graph(self):
        return self.chart


Myapp().run()
