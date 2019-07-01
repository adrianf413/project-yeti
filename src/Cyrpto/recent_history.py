from pycoingecko import CoinGeckoAPI
import datetime
import time
import json

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

def get_last_twelve_hours_prices(coin_list):
    # main method
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
    coin_storage = open("coins.txt", 'w+')
    counter = 0
    coin_list_ids = ['bitcoin', 'bitcoin-cash', 'ethereum', 'litecoin', 'ripple', 'eos',
                    'binancecoin', 'cardano', 'tether', 'stellar','tron', 'cosmos', 
                    'dogecoin']
                    
    get_last_twelve_hours_prices(coin_list_ids)


    while True:
        break
        current_time = datetime.datetime.now()

        if current_time.second == 0:
            print(current_time)
            #time.sleep(58)
            x = current_time.strftime('%Y-%m-%d %H:%M:%S')
            #print(x)
            current = cg.get_price('bitcoin', 'eur')
            #print(current)
            print(x)
            coin_history.append({x:current})
            coin_storage.write(json.dumps({x:current}))
            coin_storage.write('\n')
            counter = counter + 1
            time.sleep(2)
            
            
        if counter == 30:
            break
        #break
        


if __name__ == '__main__':
    main()
