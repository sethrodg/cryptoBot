import os
import time
import requests
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout


class MyLayout(GridLayout):
    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)
        self.cols = 4
        self.add_widget(Label(text = "cryptoBot"))
        
        

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


    active = False
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


        

        

        
        


      






def main():

    tickers = ["btc"]
    for t in tickers:
        modelOne(t)



#main()
if __name__ == "__main__":
    MyApp().run()