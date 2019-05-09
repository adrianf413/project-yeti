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
        thirty_mins_ago = current_time - datetime.timedelta(minutes = 30)
        hour_ago = current_time - datetime.timedelta(hours = 1)
        six_hours_ago = current_time - datetime.timedelta(hours = 6)
        twelve_hours_ago = current_time - datetime.timedelta(hours = 12)

        print(thirty_mins_ago.strftime('%Y-%m-%d %H:%M:%S'))
        print(hour_ago.strftime('%Y-%m-%d %H:%M:%S'))
        print(six_hours_ago.strftime('%Y-%m-%d %H:%M:%S'))
        print(twelve_hours_ago.strftime('%Y-%m-%d %H:%M:%S'))
        
        break
        if current_time.second == 0:
            print(current_time)
            time.sleep(58)


if __name__ == '__main__':
    main()
