from pycoingecko import CoinGeckoAPI
import json

def main():
    print("Getting crypto currency data now")
    cg = CoinGeckoAPI()
    f = open("coins.txt", 'w+')
    coins = cg.get_coins_list()
    for i in coins:
        f.write(json.dumps(i))
    #coins = cg.get_coin_status_updates_by_id('bitcoin')
    #exch = cg.get_exchange_rates()
    bitcoin = cg.get_price('bitcoin', 'eur')
    ethereum = cg.get_price('ethereum', 'eur')
    xrp = cg.get_price('ripple', 'eur')
    eos = cg.get_price('eos', 'eur')
    bitcoincash = cg.get_price('bitcoin-cash', 'eur')
    litecoin = cg.get_price('litecoin', 'eur')
    binancecoin = cg.get_price('binancecoin', 'eur')
    cardano = cg.get_price('cardano', 'eur')
    tether = cg.get_price('tether', 'eur')
    stellar = cg.get_price('stellar', 'eur')
    tron = cg.get_price('tron', 'eur')
    cosmos = cg.get_price('cosmos', 'eur')
    dogecoin = cg.get_price('dogecoin', 'eur')

    print(bitcoin)
    print(ethereum)
    print(xrp)
    print(eos)
    print(bitcoincash)
    print(litecoin)
    print(binancecoin)
    print(cardano)
    print(tether)
    print(stellar)
    print(tron)
    print(cosmos)
    print(dogecoin)
    #print(exch)
    #print(len(coins))
    #print(coins)
    #for i in coins:
    #    print(i)

if __name__ == '__main__':
    main()
