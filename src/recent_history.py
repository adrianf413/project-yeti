from pycoingecko import CoinGeckoAPI
import datetime
import time


def main():
    # main method
    cg = CoinGeckoAPI()

    while True:
        current_time = datetime.datetime.now()
        x = current_time.strftime('%Y-%m-%d %H:%M:%S')
        print(x)
        if current_time.second == 0:
            print(current_time)
            time.sleep(58)


if __name__ == '__main__':
    main()
