from pycoingecko import CoinGeckoAPI
import json

print("Getting crypto currency data now")
cg = CoinGeckoAPI()


def get_monthly_increase(id, currency, date):
    current = cg.get_price(id, currency)
    old = cg.get_coin_history_by_id(id, date)
    current_euro = current[id][currency]
    old_euro = old['market_data']['current_price'][currency]
    return ((current_euro/old_euro) - 1)*100


#def get_day_increase():


def main():

    f = open("coins.txt", 'w+')
    coins = cg.get_coins_list()
    for i in coins:
        f.write(json.dumps(i))
    #coins = cg.get_coin_status_updates_by_id('bitcoin')
    #exch = cg.get_exchange_rates()
    bitcoin = cg.get_price('bitcoin', 'eur')
    #ethereum = cg.get_price('ethereum', 'eur')
    #xrp = cg.get_price('ripple', 'eur')
    #eos = cg.get_price('eos', 'eur')
    #bitcoincash = cg.get_price('bitcoin-cash', 'eur')
    #litecoin = cg.get_price('litecoin', 'eur')
    #binancecoin = cg.get_price('binancecoin', 'eur')
    #cardano = cg.get_price('cardano', 'eur')
    #tether = cg.get_price('tether', 'eur')
    #stellar = cg.get_price('stellar', 'eur')
    #tron = cg.get_price('tron', 'eur')
    #cosmos = cg.get_price('cosmos', 'eur')
    #dogecoin = cg.get_price('dogecoin', 'eur')
    coin_id_list = ['bitcoin', 'ethereum', 'ripple', 'eos', 'bitcoin-cash',
                    'litecoin', 'binancecoin', 'cardano', 'tether', 'stellar',
                    'tron', 'cosmos', 'dogecoin']
    print(bitcoin['bitcoin']['eur'])
    #print(ethereum)
    #print(xrp)
    #print(eos)
    #print(bitcoincash)
    #print(litecoin)
    #print(binancecoin)
    #print(cardano)
    #print(tether)
    #print(stellar)
    #print(tron)
    #print(cosmos)
    #print(dogecoin)

    bitcoin_yesterday = cg.get_coin_history_by_id('bitcoin', '01-04-2019' )

    #for i in range(0, 7):

    print(bitcoin_yesterday['market_data']['current_price']['eur'])
    today = bitcoin['bitcoin']['eur']
    yesterday = bitcoin_yesterday['market_data']['current_price']['eur']
    percentage_diff = ((today/yesterday) - 1)*100
    print("Percentage increase since 1st of April: " + str(percentage_diff))

    print("Testing function now\n\n")
    for x in coin_id_list:
        def_test = get_monthly_increase(x, 'eur', '01-04-2019')
        print(x + " : " + str(def_test))


if __name__ == '__main__':
    main()
