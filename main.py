from multiprocessing.dummy import active_children
import os
import time
from turtle import color, onclick
import requests

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.core.window import Window




class MyLayout(GridLayout):


    def getPrice():
        response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
        data = response.json()
        price = data["bpi"]["USD"]["rate"]
        price = float(price.replace(',', ''))
        return price

    def __init__(self, **kwargs):

        super(MyLayout, self).__init__(**kwargs)
        self.cols = 2
        self.active = "Inactive"

        self.active_label = Label(text = self.active, color = [1, 0, 0, 1])
        self.add_widget(self.active_label)

        self.label_one = Label(text = "Price")
        self.add_widget(self.label_one)

        self.label_two = Label(text = "Two")
        self.add_widget(self.label_two)
        
        self.button_one = Button(text= "On/Off")
        self.button_one.bind(on_press = self.pressed_one)
        self.add_widget(self.button_one)


    def pressed_one(self, instance):
        running = self.active_label.text
    
        if running == "Inactive":
            self.active_label.text = "Active"
            self.active_label.color = [0, 1, 0, 1]

            price_text = "BTC: $" + str(getPrice())
            self.label_one.text = (price_text)

        else:
            self.active_label.text  = "Inactive"
            self.active_label.color = [1, 0, 0, 1]
        
        

class MyApp(App):
    def build(self): 
        return MyLayout()





def getPrice():
    response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
    data = response.json()
    price = data["bpi"]["USD"]["rate"]
    price = float(price.replace(',', ''))
    return price


def buy(tick, amt):
    print("buy", amt, tick)


def sell(tick, amt):
    print("sell", amt, tick)


def modelOne(tick):
    lowerBound = 61150
    upperBound = 62800
    stop = 0

    pricePaid = 0
    priceSold = 0
    
    while not active:
        currPrice = getPrice()
        print("btc: ", currPrice)

        if currPrice < lowerBound:
            buy("btc", 1)
            pricePaid = currPrice
            stop = pricePaid * (0.99)
            active = True

        time.sleep(1000)        
    
    while active:
        time.sleep(1000)
        currPrice = getPrice()
        
        print("btc: ", currPrice, "  stop: ", stop)
        
        if currPrice > upperBound or currPrice <= stop:
            sell("btc", 1)
            active = False
            priceSold = currPrice
            profit = priceSold-pricePaid
            pret = (profit / pricePaid) * 100
            print("sold for ", profit, "profit", " at a ", pret, "% return")
            priceSold, pricePaid = 0, 0

        else:
            #update stop price to curr price if we're green
            if stop == (pricePaid * (0.99)) and currPrice > (pricePaid+50):
                stop = currPrice-50
                print("STOP UPDATED (GREEN)")




    




if __name__ == "__main__":
    MyApp().run()

    '''
    tickers = ["btc"]
    for t in tickers:
        modelOne(t)
    '''