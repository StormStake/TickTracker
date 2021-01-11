import requests
import sys


from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
import jsonhelper
from kivy_garden.graph import Graph, MeshLinePlot

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


class thisApp(App):

    def update_xaxis(self,*args):
        #unknown if need at this point
        self.graph
        self.cnt
        #graph.xmin = 0
        #graph.xmax = cnt


    def update_points(self, *args):
        self.i
        self.MYLIST
        self.cnt
        self.plot
        self.plot.points = self.getPointsFromApi()

    def getPointsFromApi(self):
        return jsonhelper.getpoints()


    def build(self):
        #init stuff
        self.graph = Graph(xlabel='Time', ylabel='Price', x_ticks_minor=0,
              x_ticks_major=10,
              y_ticks_major=10,
              y_grid_label=True,
              x_grid_label=True,
              padding=5,
              x_grid=True,
              y_grid=True,
              xmin=0,
              xmax=30,
              ymin=0,
              ymax=50)


        self.plot = MeshLinePlot(color=[1, 0, 0, 1])
        self.plot.points = self.getPointsFromApi()
        self.graph.add_plot(self.plot)

        self.i = 0
        self.cnt = 100
        self.MYLIST = []


        Clock.schedule_interval(self.update_points, 1/60.)
        Clock.schedule_interval(self.update_xaxis, 1/60.)


        return(self.graph)

thisApp().run()
