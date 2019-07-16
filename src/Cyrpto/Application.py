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

# creating an instance of the coin gecko API to get retrieve coin data
cg = CoinGeckoAPI()

def main():

    # List of IDs for the 13 coind that we are starting with 
    coin_id_list = ['bitcoin', 'bitcoin-cash', 'ethereum', 'litecoin', 'ripple', 'eos',
                    'binancecoin', 'cardano', 'tether', 'stellar','tron', 'cosmos', 
                    'dogecoin']
    
    # Initialising the list of Coin objects.
    coin_object_list = []
    for i in coin_id_list:
        coin_object_list.append(Coin(i, cg.get_price(i, 'eur')))

    #for j in coin_object_list:
    #    print(j.id)
    #    print(j.price)

    # initialise the coin data for the previous 24 hours
    print("Initiating coins")
    rh.initiate_coin_history(coin_id_list)

while True:
    print("Enterred infinite loop")
	# monitor the input from the coin analytics
    break
    
    # monitor the input from the reddit analytics


    # make a decision based on the analytics inputs
 

    # if theres a positive response from analytics
    # Excecute exchange code for selected Coin

if __name__ == '__main__':
    main()
