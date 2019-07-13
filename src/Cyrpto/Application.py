"""
This is the applications main class, 
which will be used to call the reddit and
coin gecko classes.

"""
from coin import Coin
import CoinGecko
import time
import datetime

# This is a skeleton class that will be populated once all the parts
# of the project are working

def main():

    # List of IDs for the 13 coind that we are starting with 
    coin_id_list = ['bitcoin', 'bitcoin-cash', 'ethereum', 'litecoin', 'ripple', 'eos',
                    'binancecoin', 'cardano', 'tether', 'stellar','tron', 'cosmos', 
                    'dogecoin']
    
    # Initialising the list of Coin objects.
    coin_object_list = []
    for i in coin_id_list:
        coin_object_list.append(Coin(i))

    # initialise the coin data for the previous 24 hours

while True:

	# monitor the input from the coin analytics
	
    
    # monitor the input from the reddit analytics


    # make a decision based on the analytics inputs
 

    # if theres a positive response from analytics
    # Excecute exchange code for selected Coin

if __name__ == '__main__':
    main()
