from pycoingecko import CoinGeckoAPI
import json
import datetime
import pandas as pd

print("Getting crypto currency data now")
cg = CoinGeckoAPI()
today_date = datetime.datetime.now()

def get_percentage_difference_by_time(id, currency, date):
    current = cg.get_price(id, currency)
    old = cg.get_coin_history_by_id(id, date)
    current_euro = current[id][currency]
    old_euro = old['market_data']['current_price'][currency]
    return ((current_euro/old_euro) - 1)*100



def main():

    fil = open("coins.txt", 'w+')
    coins = cg.get_coins_list()
    bitcoin = cg.get_price('bitcoin', 'eur')
    output = pd.DataFrame()
    coin_id_list = ['bitcoin', 'bitcoin-cash', 'ethereum', 'litecoin', 'ripple', 'eos',
                     'binancecoin', 'cardano', 'tether', 'stellar',
                    'tron', 'cosmos', 'dogecoin']

    print("Testing function now\n\n")
    month_percent_list = []
    week_percent_list = []
    day_percent_list = []
    week_time_diff = datetime.timedelta(days = 7)
    day_time_diff = datetime.timedelta(days = 1)
    month_time_diff = datetime.timedelta(days = 30)

    prices = []
    for x in coin_id_list:
        prices.append(cg.get_price(x, 'eur'))

        date = today_date - day_time_diff
        f = date.strftime('%d-%m-%Y')
        def_test = get_percentage_difference_by_time(x, 'eur', f)
        day_percent_list.append({x:def_test})

        date = today_date - week_time_diff
        f = date.strftime('%d-%m-%Y')
        def_test = get_percentage_difference_by_time(x, 'eur', f)
        week_percent_list.append({x:def_test})

        date = today_date - month_time_diff
        f = date.strftime('%d-%m-%Y')
        def_test = get_percentage_difference_by_time(x, 'eur', f)
        month_percent_list.append({x:def_test})

    #percent_list.sort(reverse=True)
    fil.write("\nCurrent Prices: Euro\n")
    for j in prices:
        fil.write(json.dumps(j))
        fil.write("\n")

    fil.write("\nDay Percentage differences:\n")
    #print(day_percent_list)
    counter = -1
    for z in day_percent_list:
        #print(z)
        fil.write(json.dumps(z))
        #fil.write(z)
        fil.write("\n")
        for key in z.keys():
            key_val = key
        for val in z.values():
            val_val = val
        print(val_val)
        output[key_val] = 5
        #counter = counter + 1
        #output.insert(counter, key_val, val_val)
        #output.assign(key_val=val_val)

    #currencies_df = {'currencies': day_percent_list}


    fil.write("\nweek Percentage differences:\n")
    for z in week_percent_list:
        #print(z)
        fil.write(json.dumps(z))
        #fil.write(z)
        fil.write("\n")

    fil.write("\nMonth Percentage differences:\n")
    for z in month_percent_list:
        #print(z)
        #print(z.keys())

        fil.write(json.dumps(z))
        #fil.write(z)
        fil.write("\n")

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(output)
    #fil.write(str(output.head()))

if __name__ == '__main__':
    main()
