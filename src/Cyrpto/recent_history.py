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

# This function will be used by the analytics class later
# This is just experimentation for now
def get_time_deltas():
    current_time = datetime.datetime.now()
    x = current_time.strftime('%Y-%m-%d %H:%M:%S')
    one_minute_ago = current_time - datetime.timedelta(minutes = 1)
    ten_minutes_ago = current_time - datetime.timedelta(minutes = 10)
    thirty_minutes_ago = current_time - datetime.timedelta(minutes = 30)
    hour_ago = current_time - datetime.timedelta(hours = 1)
    six_hours_ago = current_time - datetime.timedelta(hours = 6)
    twelve_hours_ago = current_time - datetime.timedelta(hours = 12)
    #print(one_minute_ago.strftime('%Y-%m-%d %H:%M:%S'))
    #print(ten_minutes_ago.strftime('%Y-%m-%d %H:%M:%S'))
    #print(thirty_minutes_ago.strftime('%Y-%m-%d %H:%M:%S'))
    #print(hour_ago.strftime('%Y-%m-%d %H:%M:%S'))
    #print(six_hours_ago.strftime('%Y-%m-%d %H:%M:%S'))
    #print(twelve_hours_ago.strftime('%Y-%m-%d %H:%M:%S'))


# WORK IN PROGRESS
# This method will find the price for a specific time 24
# hours ago, and replace it with the new price
def update_recent_prices(coin_objects):
    for i in coin_objects:
        if i.timestamp == '21:00':
            # 21:00 is a random time I used for testing
            i.price = 0
            break

# THis is more than likely a dead/old function, 
# No need to review, just keeping incase theres something in
# I need from it
def get_last_twelve_hours_prices(coin_list):
    print("getting last minutes data for all coins")
    cg = CoinGeckoAPI()
    coin_history = []
    coin_storage = open("coins.txt", 'w+')
    counter = 0

    while True:
        for i in coin_list:
            current_time = datetime.datetime.now()

            if (current_time.second%1) == 0:
                print(current_time)
                #time.sleep(58)
                x = current_time.strftime('%Y-%m-%d %H:%M:%S')
                #print(x)
                current = cg.get_price(i, 'eur')
                #print(current)
                print(x)
                coin_history.append({x:current})
                coin_storage.write(json.dumps({x:current}))
                coin_storage.write('\n')
                counter = counter + 1
        time.sleep(30)
        coin_storage.write('\n\n')
                
            #if counter == 30:
            #    break
            #break

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
