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
import reqhelp
import RPi.GPIO as GPIO
import time

pindt = 0

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

        #rpi setup
        channels = [17,22,23,27]
        GPIO.setmode(GPIO.BCM)
        for channel in channels:
            GPIO.setup(channel, GPIO.OUT)
            GPIO.output(channel, GPIO.HIGH)




        #for fullscreen use
        Window.fullscreen = 'auto'
        

        tickers = [
                    'IBM',
                    'AAPL',
                    'INTC',
                    'BINANCE:BTCUSDT'
                    ]

        pages = []
        pageslay = PageLayout(border="20")


        for i in range(len(tickers)):
            pages.append(GraphPage(tickers[i]))
        for i in range(len(pages)):
            pageslay.add_widget(pages[i].getWidget())


        requer = reqhelp.helper()

        requer.changeTimeSpan('W')
        requer.ChangeResolution(30)
        for ticker in tickers:
            requer.addtotargets(ticker)

        requer.start()

        def update(*rap):

            for page in pages:
                data = requer.getdata(page.getTicker())

                if data != 0:
                    page.getchart().update(data)
                    page.Currentpricelabel.text = f'Current Quote:\n {str(round(page.getchart().CurrentPrice,2))}'

        
        def checkpins(self):

            global pindt

            if GPIO.input(17) == 0:
                if time.time() - pindt > 0.2:
                    if pageslay.page < 4:
                        pageslay.page += 1
                pindt = time.time()
            if GPIO.input(22) == 0:
                if time.time() - pindt > 0.2:
                    if pageslay.page > 0:
                        pageslay.page -= 1
                pindt = time.time()

        Clock.schedule_interval(update, 1/30)
        Clock.schedule_interval(checkpins, 1/20)
        return pageslay



class GraphPage():
    def __init__(self, ticker):

        self.chart = linechart(ticker)
        self.ticker = ticker
        self.Page = MyBox(orientation="vertical")
        self.Currentpricelabel = Label(text=f'Current Quote:\n {str(round(self.chart.CurrentPrice, 2))}', font_size='35sp')
        #Upper Layout
        upperLayout = MyBox(orientation="horizontal")
        upperLayout.add_widget(self.Currentpricelabel)


        try:
            upperLayout.add_widget(MyImage(source=f"./Images/{''.join(ticker.split(':'))}.png"))
        except:
            upperLayout.add_widget(MyImage(source=f'./Images/NA.png'))
        #Lower Layout
        self.Page.add_widget(upperLayout)
        self.Page.add_widget(self.chart.Get_graph())
    def getWidget(self):
        return self.Page

    def getchart(self):
        return self.chart

    def getTicker(self):
        return self.ticker

class linechart():
    def __init__(self, ticker):
        self.CurrentPrice = 100
        self.ticker = ticker
        self.cryptos = []
        self.yticks = 100



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




    def update(self, data):

        self.CurrentPrice = data['CurrentPrice']
        try:
            #sizing graph adding upper buffer
            self.chart.ymax = round((data['ymax']+data['ymax']/4)/10)*10
            self.chart.ymin = round((data['ymin']-data['ymin']/4)/10)*10
            #sizing xmax
            self.xmax = len(data['plot'])

            self.plots = data['plot']

            self.yticks = (self.chart.ymax - self.chart.ymin)/4
            self.chart.y_ticks_major = self.yticks
            self.plot.points = self.plots
            self.xmax = len(self.plot.points)-1
            self.chart.xmax = self.xmax
        except:
            pass



    def Get_graph(self):
        return self.chart


Myapp().run()
