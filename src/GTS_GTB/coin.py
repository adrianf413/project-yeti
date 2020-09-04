'''
This is the coin class, which will be used to 
store the data for the coins, with each object 
holding the id, price and time. 

'''

import time
import datetime
import json


class Coin:
    def __init__(self, id, price):
        # Creating the attributes of interest for the coins
        self.id = id
        self.price = price[id]['eur']
        self.timestamp = 0
        self.one_minute_percentage = 0
        self.ten_minute_percentage = 0
        self.thirty_minute_percentage = 0
        self.one_hour_percentage = 0
        self.six_hour_percentage = 0
        self.twelve_hour_percentage = 0
        self.one_day_percentage = 0
        self.one_week_percentage = 0
        self.one_month_percentage = 0
        self.currently_bought = False
