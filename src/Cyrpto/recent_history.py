'''
This is the script for finding and storuing 
coin data for the previous 24 hours upon 
initial start up.
'''

from pycoingecko import CoinGeckoAPI
import datetime
import time
import json
from coin import Coin

cg = CoinGeckoAPI()
# List used to store objects that will hold the prices
# For the last 24 hours. 
coin_history_objects = []
coin_storage = open("12hourstorage.txt", 'w+')

def initiate_coin_history(coin_id_list):
    # Getting and storing the price every minute for 24 hours
    counter = 0
    while counter < (3):
        if datetime.datetime.now().second == 0:
            for i in coin_id_list:
                current_time = datetime.datetime.now()
                time_value = current_time.strftime('%H:%M')
                price = cg.get_price(i, 'eur')
                temp_coin_object = Coin(i, price)
                temp_coin_object.timestamp = time_value
                # stoting list of Coin objects
                coin_history_objects.append(temp_coin_object)
            counter = counter + 1
    print("Done writing 3 mintutes worth of data")
    for l in coin_history_objects:
        coin_storage.write(l.id + ' ' + str(l.price) + ' ' + str(l.timestamp) + '\n')  


# Method to populate the current price attribute of the coin objects
def get_current_price(id):
    current_price = cg.get_price(id, 'eur')
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
    key_value = one_minute_ago.strftime('%H:%M')
    for q in coin_history_objects:
        if q.id == id and q.timestamp == key_value:
            return ((current_price/q.price)-1) * 100

def get_thirty_minute_percentage(id, current_price):
    current_time = datetime.datetime.now()
    thirty_minutes_ago = current_time - datetime.timedelta(minutes = 30)
    key_value = one_minute_ago.strftime('%H:%M')
    for q in coin_history_objects:
        if q.id == id and q.timestamp == key_value:
            return ((current_price/q.price)-1) * 100

def get_one_hour_percentage(id, current_price):
    current_time = datetime.datetime.now()
    one_hour_ago = current_time - datetime.timedelta(hours = 1)
    key_value = one_minute_ago.strftime('%H:%M')
    for q in coin_history_objects:
        if q.id == id and q.timestamp == key_value:
            return ((current_price/q.price)-1) * 100

def get_six_hour_percentage(id, current_price):
    current_time = datetime.datetime.now()
    six_hours_ago = current_time - datetime.timedelta(hours = 6)
    key_value = one_minute_ago.strftime('%H:%M')
    for q in coin_history_objects:
        if q.id == id and q.timestamp == key_value:
            return ((current_price/q.price)-1) * 100

def get_twelve_hour_percentage(id, current_price):
    current_time = datetime.datetime.now()
    twelve_hours_ago = current_time - datetime.timedelta(hours = 12)
    key_value = one_minute_ago.strftime('%H:%M')
    for q in coin_history_objects:
        if q.id == id and q.timestamp == key_value:
            return ((current_price/q.price)-1) * 100

def get_one_day_percentage(id, current_price):
    current_time = datetime.datetime.now()
    one_day_ago = current_time - datetime.timedelta(days = 1)
    key_value = one_minute_ago.strftime('%d-%m-%Y')
    for q in coin_history_objects:
        if q.id == id and q.timestamp == key_value:
            return ((current_price/q.price)-1) * 100

def get_one_week_percentage(id, current_price):
    current_time = datetime.datetime.now()
    one_week_ago = current_time - datetime.timedelta(days = 7)
    key_value = one_minute_ago.strftime('%d-%m-%Y')
    for q in coin_history_objects:
        if q.id == id and q.timestamp == key_value:
            return ((current_price/q.price)-1) * 100

def get_one_month_percentage(id, current_price):
    current_time = datetime.datetime.now()
    one_month_ago = current_time - datetime.timedelta(days = 28)
    key_value = one_minute_ago.strftime('%d-%m-%Y')
    for q in coin_history_objects:
        if q.id == id and q.timestamp == key_value:
            return ((current_price/q.price)-1) * 100

# WORK IN PROGRESS
# This method will find the price for a specific time 24
# hours ago, and replace it with the new price
def update_recent_prices(time):
    for i in coin_history_objects:
        if i.timestamp == time:
            # Rewriting old time with new time. 
            i.price = cg.get_price(i.id, 'eur')
            

def main():
    # main method
    cg = CoinGeckoAPI()
    coin_history = []
    coin_storage = open("12hourstorage.txt", 'w+')
    counter = 0
    coin_objects = []
    coin_list_ids = ['bitcoin', 'bitcoin-cash', 'ethereum', 'litecoin', 'ripple', 'eos',
                    'binancecoin', 'cardano', 'tether', 'stellar','tron', 'cosmos', 
                    'dogecoin']
    current_time = datetime.datetime.now()
    counter = 0

    # Getting and storing the price every minute for 5 minutes
    # As a test 
    while counter < 5:
        if datetime.datetime.now().second == 0:
            for i in coin_list_ids:
                z = current_time.strftime('%H:%M:%S')
                price = cg.get_price(i, 'eur')
                # stoting list of Coin objects
                # Coin obbject is in coin.py
                coin_objects.append(Coin(i, price[i]['eur'], datetime.datetime.now()))
            counter = counter + 1

    # Writing 5 minute data to local storage for debugging puposes        
    for l in coin_objects:
        coin_storage.write(l.id + ' ' + str(l.price) + ' ' + str(l.timestamp) + '\n')  


if __name__ == '__main__':
    main()
