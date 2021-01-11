import requests
import sys

from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy_garden.graph import Graph, LinePlot
from kivy.core.window import Window

import jsonhelper



class Myapp(App):

    #App Entry Point
    def build(self):
        #self.CurrentPrice = 0
        #init stuff
        Window.fullscreen = 'auto'
        #layout setup
        linegraph = linechart()
        layout = BoxLayout(orientation="vertical")
        #upper layout
        upperLayout = BoxLayout(orientation="horizontal")

        upperLayout.add_widget(Label(text=str(round(linegraph.CurrentPrice, 2)), font_size='200sp'))
        upperLayout.add_widget(Image(source='IBM.svg.png'))
        #lower layout
        layout.add_widget(upperLayout)
        layout.add_widget(linegraph.get_points())


        return layout


class linechart():
    def __init__(self):
        self.CurrentPrice = 0
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
            xmax=51,
            ymin=0,
            
            )


        self.plot = LinePlot(color=[1, 0, 0, 1],line_width=2)
        self.plot.points = self.getPointsFromApi()
        self.graph.add_plot(self.plot)

        self.i = 0
        self.cnt = 100
        self.MYLIST = []


        Clock.schedule_interval(self.update_points, 1/60.)







    def update_points(self, *args):
        self.plot.points = self.plots


    def getPointsFromApi(self):
        data = jsonhelper.getpointsstock('AAPL', 'bvtss4748v6pijnevmqg')
        #sizing graph adding upper buffer
        #TODO Make buffer round
        self.graph.ymax = data['ymax']+data['ymax']/4
        self.plots = data['plot']
        self.CurrentPrice = data['CurrentPrice']
        return data['plot']


    def get_points(self):
        return self.graph


Myapp().run()
