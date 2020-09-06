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
import json


# Set the logging congfiguration
logging.basicConfig(filename='crypto_service.log', level=logging.INFO, filemode='w', format='[%(asctime)s][%(name)-6s][%(levelname)-4s] %(message)s', datefmt='%d-%m-%Y %H:%M:%S')

# creating an instance of the coin gecko API to get retrieve coin data
cg = CoinGeckoAPI()

coin_storage = open("12hourstorage.json", 'w')

coin_history_objects =[]

def setup_coin_data_file(coin_id_list):
    for coin in coin_id_list:
        price = cg.get_price(coin, 'eur')
        coin_history_objects.append(Coin(coin, price))
    
    json_string = json.dumps([ob.__dict__ for ob in coin_history_objects])
    print(json_string)
    coin_storage.write(json_string)
    coin_storage.close()

def update_coin_data_file(coin_id_list):
    print("Updating coin json file")
    # Need to clear the list of objects to avoid duplication
    coin_history_objects.clear()
    for coin in coin_id_list:
        #print(coin)
        d_price = cg.get_price(coin, 'eur')
        price = d_price[coin]['eur']
        #print(price)
        temp_coin = Coin(coin, d_price)
        #print(rh.get_one_minute_percentage(coin, price))
        temp_coin.one_minute_percentage = rh.get_one_minute_percentage(coin, price)
        temp_coin.ten_minute_percentage = rh.get_ten_minute_percentage(coin, price)
        temp_coin.thirty_minute_percentage = rh.get_thirty_minute_percentage(coin, price)
        temp_coin.one_hour_percentage = rh.get_one_hour_percentage(coin, price)
        temp_coin.six_hour_percentage = rh.get_six_hour_percentage(coin, price)
        temp_coin.twelve_hour_percentage = rh.get_twelve_hour_percentage(coin, price)
        temp_coin.one_day_percentage = rh.get_one_day_percentage(coin, price)
        temp_coin.one_week_percentage = rh.get_one_week_percentage(coin, price)
        temp_coin.one_month_percentage = rh.get_one_month_percentage(coin, price)
        temp_coin.timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        coin_history_objects.append(temp_coin)
    
    json_string = json.dumps([ob.__dict__ for ob in coin_history_objects])
    print(json_string)
    
    coin_storage = open("12hourstorage.json", 'w')
    coin_storage.write(json_string)
    coin_storage.close()



def main():

    logging.info("Started crypto historical data service")

    # List of IDs for the 13 coind that we are starting with 
    coin_id_list = ['bitcoin', 'bitcoin-cash', 'ethereum', 'litecoin', 'ripple', 'eos',
                    'binancecoin', 'cardano', 'tether', 'stellar','tron', 'cosmos', 
                    'dogecoin']

    
    # List to store the results of the GTB/GTS equation
    gts_gtb_list = []

    #for j in coin_object_list:
    #    print(j.id)
    #    print(j.price)

    # initialise the coin storage file for the previous 24 hours
    logging.info("Initiating coin data JSON file")
    
    
    setup_coin_data_file(coin_id_list)
    logging.info("Coin data file initiated.")

    # Initialising the list of Coin objects in recent history script.
    logging.info("Creating coin history object list in recent history module")
    rh.initiate_coin_data_list(coin_id_list)
    logging.info("Coin history object list instantiated in recent history helper module")

    logging.info("Setup complete, starting infinite loop.")

    while True:
        #return
        # update the coin storage file

        update = True
        while update:
            if datetime.datetime.now().second == 0:
                # Update each new minute
                logging.info("Updating coin information for this minute")
                time = datetime.datetime.now()
                time_to_update = time.strftime('%H:%M')
                for coin_id in coin_id_list:
                    try:
                        rh.update_recent_prices(time_to_update, coin_id)
                    except Exception as e:
                        logging.error("Error updating coin history for this minute")
                        logging.info(e)
                update = False
        
        
        # Now need to update the file with the newest coin data 
        try:
            update_coin_data_file(coin_id_list)
        except Exception as e:
            logging.error("Error updating coin data in JSON file")
            logging.error(e)
        logging.info("Finished updating stored data for each coin")
        gts_gtb_list.clear()

if __name__ == '__main__':
    main()
