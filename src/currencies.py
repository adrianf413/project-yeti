from pycoingecko import CoinGeckoAPI
import json
import datetime

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

    coin_id_list = ['bitcoin', 'ethereum', 'ripple', 'eos', 'bitcoin-cash',
                    'litecoin', 'binancecoin', 'cardano', 'tether', 'stellar',
                    'tron', 'cosmos', 'dogecoin']

    print("Testing function now\n\n")
    month_percent_list = []
    week_percent_list = []
    day_percent_list = []
    week_time_diff = datetime.timedelta(days = 7)
    day_time_diff = datetime.timedelta(days = 1)
    month_time_diff = datetime.timedelta(days = 30)
    for x in coin_id_list:
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
    fil.write("\nDay Percentage differences:\n")
    for z in day_percent_list:
        #print(z)
        fil.write(json.dumps(z))
        #fil.write(z)
        fil.write("\n")

    fil.write("\nweek Percentage differences:\n")
    for z in week_percent_list:
        #print(z)
        fil.write(json.dumps(z))
        #fil.write(z)
        fil.write("\n")

    fil.write("\nMonth Percentage differences:\n")
    for z in month_percent_list:
        #print(z)
        fil.write(json.dumps(z))
        #fil.write(z)
        fil.write("\n")


if __name__ == '__main__':
    main()
