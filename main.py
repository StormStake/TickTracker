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
        Window.size = (1920,1080)
        Window.clearcolor = (0.1,0.1,0.1,1)
        #layout setup

        pageslay = PageLayout(border="20")

        Page1 = GraphPage('IBM')
        Page2 = GraphPage('AAPL')
        Page3 = GraphPage('BINANCE:BTCUSDT')
        pages = [Page1, Page2, Page3]
        pageslay.add_widget(Page1.getWidget())
        pageslay.add_widget(Page2.getWidget())
        pageslay.add_widget(Page3.getWidget())
        def update(passs):
            for page in pages:
                page.getchart().update_points()
        Clock.schedule_interval(update, 1/30.)
        return pageslay


class GraphPage():
    def __init__(self, ticker):

        self.chart = linechart(ticker)

        self.Page = MyBox(orientation="vertical")

        #Upper Layout
        upperLayout = MyBox(orientation="horizontal")
        upperLayout.add_widget(Label(text=f'Current Quote:\n {str(round(self.chart.CurrentPrice, 2))}', font_size='100sp'))
        try:
            upperLayout.add_widget(MyImage(source=f'{ticker}.png'))
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
        self.ticker = ticker
        self.cryptos = []
        self.yticks = 100
        for dicto in json.loads(requests.get('https://finnhub.io/api/v1/crypto/symbol?exchange=binance&token=bvtss4748v6pijnevmqg').text):

            self.cryptos.append(dicto['symbol'])

        self.chart = Graph(
            xlabel='Time',
            ylabel='Price',
            x_ticks_minor=0,
            x_ticks_major=10,
            y_ticks_major=self.yticks,
            y_grid_label=True,
            x_grid_label=True,
            padding=5,
            x_grid=True,
            y_grid=True,
            xmin=0,
            xmax=51,
            ymin=0,
            )


        self.plot = SmoothLinePlot(color=[1, 1, 1, 1])
        self.plot.points = self.getPointsFromApi()
        self.chart.add_plot(self.plot)



        Clock.schedule_interval(self.getPointsFromApi, 30)


    def update_points(self):
        
        self.yticks = self.chart.ymax/3
        print(self.yticks,'\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
        self.plot.points = self.plots

    def printsomething(self):
        print('Hello World')

    def getPointsFromApi(self):
        if self.ticker in self.cryptos:
            data = jsonhelper.getCrytpoPlot(self.ticker, 'bvtss4748v6pijnevmqg')
        else:
            data = jsonhelper.GetStockPlot(self.ticker, 'bvtss4748v6pijnevmqg')
        #sizing graph adding upper buffer
        #TODO Make buffer round
        self.chart.ymax = data['ymax']+data['ymax']/4
        self.chart.ymin = data['ymin']-data['ymin']/4
        self.plots = data['plot']
        self.CurrentPrice = data['CurrentPrice']
        return data['plot']


    def Get_graph(self):
        return self.chart


Myapp().run()
