'''
This is the script for finding and storuing 
coin data for the previous 24 hours upon 
initial start up.
'''

from pycoingecko import CoinGeckoAPI
import datetime
import time
import json
import logging
from coin import Coin

# Set the logging congfiguration
logging.basicConfig(filename='CCPB.log', level=logging.INFO, filemode='w', format='[%(asctime)s][%(name)-12s][%(levelname)-4s] %(message)s', datefmt='%d-%m-%Y %H:%M:%S')

cg = CoinGeckoAPI()
# List used to store objects that will hold the prices
# For the last 24 hours. 
coin_history_objects = []
coin_storage = open("12hourstorage.txt", 'w+')

def initiate_coin_history(coin_id_list):
    # Getting and storing the price every minute for 24 hours
    counter = 0
    logging.info("Starting to store coin data every minute")
    while counter < (24*60):
        if datetime.datetime.now().second == 0:
            for i in coin_id_list:
                try:
                    current_time = datetime.datetime.now()
                    time_value = current_time.strftime('%H:%M')
                    price = cg.get_price(i, 'eur')
                    temp_coin_object = Coin(i, price)
                    temp_coin_object.timestamp = time_value
                    # storing list of Coin objects
                    coin_history_objects.append(temp_coin_object)
                except:
                    logging.error("Error initiating coin information for " + i)
            counter = counter + 1
            logging.info("Finished storing coins for this minute")
    logging.info("Completed initiatie coins function")

# Method to populate the current price attribute of the coin objects
def get_current_price(id):
    try:
        current_price = cg.get_price(id, 'eur')
    except:
        logging.error("Error retreiving price for " + id)
        return 0
    return current_price[id]['eur']

# Methods to get the percentage differences for each time period
def get_one_minute_percentage(id, current_price):
    current_time = datetime.datetime.now()
    one_minute_ago = current_time - datetime.timedelta(minutes = 1)
    key_value = one_minute_ago.strftime('%H:%M')
    for q in coin_history_objects:
        if q.id == id and q.timestamp == key_value:
            return ((current_price/q.price)-1) * 100
            
def get_ten_minute_percentage(id, current_price):
    current_time = datetime.datetime.now()
    ten_minutes_ago = current_time - datetime.timedelta(minutes = 10)
    key_value = ten_minutes_ago.strftime('%H:%M')
    for q in coin_history_objects:
        if q.id == id and q.timestamp == key_value:
            return ((current_price/q.price)-1) * 100

def get_thirty_minute_percentage(id, current_price):
    current_time = datetime.datetime.now()
    thirty_minutes_ago = current_time - datetime.timedelta(minutes = 30)
    key_value = thirty_minutes_ago.strftime('%H:%M')
    for q in coin_history_objects:
        if q.id == id and q.timestamp == key_value:
            return ((current_price/q.price)-1) * 100

def get_one_hour_percentage(id, current_price):
    current_time = datetime.datetime.now()
    one_hour_ago = current_time - datetime.timedelta(hours = 1)
    key_value = one_hour_ago.strftime('%H:%M')
    for q in coin_history_objects:
        if q.id == id and q.timestamp == key_value:
            return ((current_price/q.price)-1) * 100

def get_six_hour_percentage(id, current_price):
    current_time = datetime.datetime.now()
    six_hours_ago = current_time - datetime.timedelta(hours = 6)
    key_value = six_hours_ago.strftime('%H:%M')
    for q in coin_history_objects:
        if q.id == id and q.timestamp == key_value:
            return ((current_price/q.price)-1) * 100

def get_twelve_hour_percentage(id, current_price):
    current_time = datetime.datetime.now()
    twelve_hours_ago = current_time - datetime.timedelta(hours = 12)
    key_value = twelve_hours_ago.strftime('%H:%M')
    for q in coin_history_objects:
        if q.id == id and q.timestamp == key_value:
            return ((current_price/q.price)-1) * 100

def get_one_day_percentage(id, current_price):
    current_time = datetime.datetime.now()
    one_day_ago = current_time - datetime.timedelta(days = 1)
    key_value = one_day_ago.strftime('%d-%m-%Y')
    old = cg.get_coin_history_by_id(id, key_value)
    old_euro = old['market_data']['current_price']['eur']
    return ((current_price/old_euro)-1) * 100

def get_one_week_percentage(id, current_price):
    current_time = datetime.datetime.now()
    one_week_ago = current_time - datetime.timedelta(days = 7)
    key_value = one_week_ago.strftime('%d-%m-%Y')
    old = cg.get_coin_history_by_id(id, key_value)
    old_euro = old['market_data']['current_price']['eur']
    return ((current_price/old_euro)-1) * 100

def get_one_month_percentage(id, current_price):
    current_time = datetime.datetime.now()
    one_month_ago = current_time - datetime.timedelta(days = 28)
    key_value = one_month_ago.strftime('%d-%m-%Y')
    old = cg.get_coin_history_by_id(id, key_value)
    old_euro = old['market_data']['current_price']['eur']
    return ((current_price/old_euro)-1) * 100

# This method will find the price for a specific time 24
# hours ago, and replace it with the new price
def update_recent_prices(time):
    for i in coin_history_objects:
        if i.timestamp == time:
            print("Old price = " + str(i.price))
            # Rewriting old time with new time. 
            logging.info("Rewriting old data with new data")
            new_price = cg.get_price(i.id, 'eur')
            i.price = new_price[i.id]['eur']
            print("New price = " + str(i.price))

