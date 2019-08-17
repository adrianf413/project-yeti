"""
This is the applications main class, 
which will be used to call the reddit and
coin gecko classes.

"""
from coin import Coin
from pycoingecko import CoinGeckoAPI
import time
import datetime
import logging
import recent_history as rh

# This is a skeleton class that will be populated once all the parts
# of the project are working

# Set the logging congfiguration
logging.basicConfig(filename='CCPB', level=logging.INFO, filemode='w', format='[%(asctime)s][%(name)-12s][%(levelname)-4s] %(message)s', datefmt='%d-%m-%Y %H:%M:%S')

# creating an instance of the coin gecko API to get retrieve coin data
cg = CoinGeckoAPI()

def main():

    logging.info("Started CryptoCurrencyPredictiveBuying application")

    # List of IDs for the 13 coind that we are starting with 
    coin_id_list = ['bitcoin', 'bitcoin-cash', 'ethereum', 'litecoin', 'ripple', 'eos',
                    'binancecoin', 'cardano', 'tether', 'stellar','tron', 'cosmos', 
                    'dogecoin']
    
    #for j in coin_object_list:
    #    print(j.id)
    #    print(j.price)

    # initialise the coin data for the previous 24 hours
    logging.info("Initiating coin data for previous 24 hours")
    rh.initiate_coin_history(coin_id_list)
    logging.info("Coin data initiated.")

    # Initialising the list of Coin objects.
    coin_object_list = []
    for i in coin_id_list:
        coin_object_list.append(Coin(i, cg.get_price(i, 'eur')))
    logging.info("Created List of coin ojects to hold various percentages")

    for i in coin_object_list:
        print(i.id + " - One muinute percentage difference is: " + str(rh.get_one_minute_percentage(i.id, i.price)))
        print(i.id + " - One day percentage difference is: " + str(rh.get_one_day_percentage(i.id, i.price)))
    #    print(i.id + " - ten muinute percentage difference is: " + str(rh.get_ten_minute_percentage(i.id, i.price)))

    while True:
        logging.info("Enterred infinite loop - about to break ..")
        # monitor the input from the coin analytics
        break
        # Dummy equation
        for i in coin_object_list:
            i.one_minute_percentage = rh.get_one_minute_percentage()
            i.ten_minute_percentage = rh.get_ten_minute_percentage()
            i.thirty_minute_percentage = rh.get_thirty_minute_percentage()
            i.one_hour_percentage = rh.get_one_hour_percentage()
            i.six_hour_percentage = rh.get_six_hour_percentage()
            i.twelve_hour_percentage = rh.get_twelve_hour_percentage()
            i.one_day_percentage = rh.get_one_day_percentage()
            i.one_week_percentage = rh.get_one_week_percentage()
            i.one_month_percentage = rh.get_one_month_percentage()
        # monitor the input from the reddit analytics


        # make a decision based on the analytics inputs
    

        # if theres a positive response from analytics
        # Excecute exchange code for selected Coin

if __name__ == '__main__':
    main()
