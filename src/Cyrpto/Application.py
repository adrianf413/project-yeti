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


# Set the logging congfiguration
logging.basicConfig(filename='CCPB.log', level=logging.INFO, filemode='w', format='[%(asctime)s][%(name)-6s][%(levelname)-4s] %(message)s', datefmt='%d-%m-%Y %H:%M:%S')

# creating an instance of the coin gecko API to get retrieve coin data
cg = CoinGeckoAPI()

def main():

    logging.info("Started CryptoCurrencyPredictiveBuying application")

    # List of IDs for the 13 coind that we are starting with 
    coin_id_list = ['bitcoin', 'bitcoin-cash', 'ethereum', 'litecoin', 'ripple', 'eos',
                    'binancecoin', 'cardano', 'tether', 'stellar','tron', 'cosmos', 
                    'dogecoin']
    
    # List to store the results of the GTB/GTS equation
    gts_gtb_list = []

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
        logging.info("Enterred infinite loop")
        # monitor the input from the coin analytics
        
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

        #for j in coin_object_list:
        #    print(j.one_minute_percentage)
        #    print(j.ten_minute_percentage) 
        #    print(j.thirty_minute_percentage)
        #    print(j.one_hour_percentage)
        #    print(j.six_hour_percentage)
        #    print(j.twelve_hour_percentage)
        #    print(j.one_day_percentage)
        #    print(j.one_week_percentage)
        #    print(j.one_month_percentage)
        
        ########################################################################
        # Putting results in to GTS/GTB Equation
        for j in coin_object_list:
            result = (j.one_minute_percentage * 3) + (j.ten_minute_percentage * 25) + (j.thirty_minute_percentage * 80) + (j.one_hour_percentage * 80) + (j.six_hour_percentage * 45) + (j.twelve_hour_percentage * 25) + (j.one_day_percentage * 10) + (j.one_week_percentage * 1) + (j.one_month_percentage * 1) 
            gts_gtb_list.append(result)

        logging.info("Printing GTS/GTB results for each coin")
        index = 0
        for i in gts_gtb_list:
            logging.info(coin_id_list[index] + ": "+  str(i))
        ########################################################################
        # monitor the input from the reddit analytics


        # make a decision based on the analytics inputs
    

        # if theres a positive response from analytics


        # Excecute exchange code for selected Coin
        # Update coin data
        logging.info("Updating stored data for each coin")
        update = True
        while update:
            if datetime.datetime.now().second == 0:
                time = datetime.datetime.now()
                time_to_update = time.strftime('%H:%M')
                try:
                    rh.update_recent_prices(time_to_update)
                except:
                    logging.error("Error updating coin history for this minute")
                    #logging.info(str(e)
                update = False
        logging.info("Finished updating stored data for each coin")

if __name__ == '__main__':
    main()
