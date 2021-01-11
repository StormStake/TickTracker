import requests
import sys

from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
import jsonhelper
from kivy_garden.graph import Graph, LinePlot
from kivy.core.window import Window
def get_price_btc():
    #returns current price of btc
    btc_api = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    api_key = 'e1c1a190-5e1d-42bd-9e88-d17213b9d2d8'

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    sess = requests.session()
    sess.headers.update(headers)
    #data = sess.get(btc_api)
    #price_in_usd = data.json()['data'][0]['quote']['USD']['price']
    #print(type(data))
    print(sys.version)
    #print(price_in_usd)
    #return(str(price_in_usd))


class Myapp(App):

    #App Entry Point
    def build(self):
        #init stuff
        Window.size = (1000,1000)
        Window.fullscreen = 'auto'
        #layout setup
        linegraph = linechart()
        layout = BoxLayout(orientation="vertical")
        #upper layout
        upperLayout = BoxLayout(orientation="horizontal")
        
        upperLayout.add_widget(Label(text=str(), font_size='200sp'))
        upperLayout.add_widget(Image(source='IBM.svg.png'))
        #lower layout
        layout.add_widget(upperLayout)
        layout.add_widget(linegraph.get_points())
        
        

        return layout


class linechart():
    def __init__(self):
        self.graph = Graph(
            xlabel='Time',
            ylabel='Price',
            x_ticks_minor=0,
            x_ticks_major=10,
            y_ticks_major=100,
            y_grid_label=True,
            x_grid_label=True,
            padding=5,
            x_grid=True,
            y_grid=True,
            xmin=0,
            xmax=50,
            ymin=0,
            ymax=1000,
            )


        self.plot = LinePlot(color=[1, 0, 0, 1],line_width=2)
        self.plot.points = self.getPointsFromApi()
        self.graph.add_plot(self.plot)

        self.i = 0
        self.cnt = 100
        self.MYLIST = []


        Clock.schedule_interval(self.update_points, 1/60.)
        Clock.schedule_interval(self.update_xaxis, 1/60.)






    def update_points(self, *args):
        self.plot.points = self.getPointsFromApi()

    def getPointsFromApi(self):

        data = jsonhelper.getpointsstock(1)
        #sizing graph adding upper buffer
        #TODO Make buffer round
        self.graph.ymax = data['ymax']+data['ymax']/4

        return data['plot']

    def get_points(self):
        return self.graph


Myapp().run()
