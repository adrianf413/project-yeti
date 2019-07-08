"""
This is the applications main class, 
which will be used to call the reddit and
coin gecko classes.

"""

import json
import datetime
import pandas as pd
import crypto_helper as ch
import time
from os import system, name
from coin import Coin

print("Getting crypto currency data now")

# getting the exact current date and time to retrieve the momentary crypto data
today_date = datetime.datetime.now()

# define our clear function 
def clear(): 

	# for windows 
	if name == 'nt': 
		_ = system('cls') 

	# for mac and linux(here, os.name is 'posix') 
	else: 
		_ = system('clear') 


def main():

    # Creating a text file to store the output, this is a temporary solution
    percentage_storage = open("coins.txt", 'w+')

    # Testing with pandas dataframe for output
    output = pd.DataFrame()

    # List of the coins we will use initially
    coin_id_list = ['bitcoin', 'bitcoin-cash', 'ethereum', 'litecoin', 'ripple', 'eos',
                    'binancecoin', 'cardano', 'tether', 'stellar','tron', 'cosmos', 
                    'dogecoin']

    # Lists to store the values for each coin
    month_percent_list = []
    week_percent_list = []
    day_percent_list = []
    prices = []
    coin_objects = []

    # Time deltas for each coin
    week_time_diff = datetime.timedelta(days = 7)
    day_time_diff = datetime.timedelta(days = 1)
    month_time_diff = datetime.timedelta(days = 30)

    # Make an instance of CoinData class
    #cd = CoinData()

    for x in coin_id_list:
        price = ch.get_prices(x, 'eur')
        coin_objects.append(Coin(x, price[x]['eur']))

    for i in coin_objects:
        print(i.id)
        print(i.price)
        print(i.timestamp)
        print('\n')

    # Loop to get the data for each coin in the list
    for x in coin_id_list:
        
        prices.append(ch.get_prices(x, 'eur'))

        date = today_date - day_time_diff
        f = date.strftime('%d-%m-%Y')
        def_test = ch.get_percentage_difference_by_time(id=x, currency='eur', date=f)
        day_percent_list.append({x:def_test})
        #print({x:def_test})

        date = today_date - week_time_diff
        f = date.strftime('%d-%m-%Y')
        def_test = ch.get_percentage_difference_by_time(id=x, currency='eur', date=f)
        week_percent_list.append({x:def_test})

        date = today_date - month_time_diff
        f = date.strftime('%d-%m-%Y')
        def_test = ch.get_percentage_difference_by_time(id=x, currency='eur', date=f)
        month_percent_list.append({x:def_test})
        
    # Writing the current prices of all the coins
    percentage_storage.write("\nCurrent Prices: Euro\n")
    for j in prices:
        percentage_storage.write(json.dumps(j))
        percentage_storage.write("\n")

    percentage_storage.write("\nDay Percentage differences:\n")
    #print(day_percent_list)
    counter = -1
    for z in day_percent_list:
        #print(z)
        percentage_storage.write(json.dumps(z))
        #percentage_storage.write(z)
        percentage_storage.write("\n")
        for key in z.keys():
            key_val = key
        for val in z.values():
            val_val = val
        #print(val_val)
        output[key_val] = 5
        #counter = counter + 1
        #output.insert(counter, key_val, val_val)
        #output.assign(key_val=val_val)

    #currencies_df = {'currencies': day_percent_list}


    percentage_storage.write("\nweek Percentage differences:\n")
    for z in week_percent_list:
        #print(z)
        percentage_storage.write(json.dumps(z))
        #percentage_storage.write(z)
        percentage_storage.write("\n")

    percentage_storage.write("\nMonth Percentage differences:\n")
    for z in month_percent_list:
        #print(z)
        #print(z.keys())

        percentage_storage.write(json.dumps(z))
        #percentage_storage.write(z)
        percentage_storage.write("\n")

    #]with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        #print(output)
    #percentage_storage.write(str(output.head()))

if __name__ == '__main__':
    main()
