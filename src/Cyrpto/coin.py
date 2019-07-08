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
        self.id = id
        self.price = price
        current_time = datetime.datetime.now()
        self.timestamp = current_time.strftime('%H:%M')
