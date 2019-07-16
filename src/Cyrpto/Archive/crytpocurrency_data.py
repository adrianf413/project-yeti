from pycoingecko import CoinGeckoAPI
import json
import datetime
import pandas as pd

print("Getting crypto currency data now")

# creating an instance of the coin gecko API to get retrieve coin data
cg = CoinGeckoAPI()


# Class to get the percentage differences using the coinGecko API
#class CoinData():

    # Constructor method
#    def __init__(self):
#        cg = CoinGeckoAPI()

# Method to get the current price of the coin
def get_price(coin_id, currency):
    return cg.get_price(coin_id, currency)

# Method to get the percentage difference for a certain coin based on a particular
# date relative to the current date and time
def get_percentage_difference_by_time(id, currency, date):

    current = cg.get_price(id, currency)
    old = cg.get_coin_history_by_id(id, date)
    current_euro = current[id][currency]
    old_euro = old['market_data']['current_price'][currency]
    return ((current_euro/old_euro) - 1)*100