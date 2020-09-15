import flask
from flask import request, jsonify, abort, render_template
from flask_bootstrap import Bootstrap
import json
import requests
import os
from coin import Coin

app = flask.Flask(__name__)
#app.config["DEBUG"] = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
bootstrap = Bootstrap(app)

@app.route('/coins/info', methods=['GET'])
def home():
    return flask.render_template('info.html')

@app.route('/coins/mpu', methods=['GET'])
def return_coin_values():
    if 'name' in request.args:
        name = request.args['name']
        
        #coin_file = open("12hourstorage.json", 'r')
        #coin_dat = json.load(coin_file)
        #loaded_json  = json.load(coin_file)
        for x in coin_dat:
            coin_id = x['id']
            #print(name)
            #print(coin_id)
            if coin_id == name:
                return flask.jsonify(x)
        abort(404)

@app.route('/coins/all', methods=['GET'])
def return_all_coin_values():
    # need to perform a request to the API and then display the result      

    # Need to read in the REST API host name in as an environment variable
    try:
        host = os.environ['API_HOSTNAME']
    except:
        host = '192.168.0.43'

    url = 'http://' + host +':5001/api/coin_data/history/all'
    coin_data = requests.get(url)
    coins = coin_data.json()
    coin_objects = []

    for coin in coins:
        #print(coin)
        temp_coin_obj = Coin(coin['id'], coin['price'])
        temp_coin_obj.timestamp = coin['timestamp']
        temp_coin_obj.one_minute_percentage = float("{:.3f}".format(coin['one_minute_percentage']))
        temp_coin_obj.ten_minute_percentage = float("{:.3f}".format(coin['ten_minute_percentage']))
        temp_coin_obj.thirty_minute_percentage = float("{:.3f}".format(coin['thirty_minute_percentage']))
        temp_coin_obj.one_hour_percentage = float("{:.3f}".format(coin['one_hour_percentage']))
        temp_coin_obj.six_hour_percentage = float("{:.3f}".format(coin['six_hour_percentage']))
        temp_coin_obj.twelve_hour_percentage = float("{:.3f}".format(coin['twelve_hour_percentage']))
        temp_coin_obj.one_day_percentage = float("{:.3f}".format(coin['one_day_percentage']))
        temp_coin_obj.one_week_percentage = float("{:.3f}".format(coin['one_week_percentage']))
        temp_coin_obj.one_month_percentage = float("{:.3f}".format(coin['one_month_percentage']))
        temp_coin_obj.market_cap = float("{:.3f}".format(coin['market_cap']))
        temp_coin_obj.volume = float("{:.3f}".format(coin['volume']))
        temp_coin_obj.currently_bought = False

        coin_objects.append(temp_coin_obj)

    return flask.render_template('coin.html', coins = coin_objects, display='All')


@app.route('/coins', methods=['GET'])
def return_specific_coin_values():
    
    # need to perform a request to the API and then display the result      
    if 'name' in request.args:
        name = request.args['name']
        url = 'http://192.168.0.43:5001/api/coin_data/history?name=' + name
        coin_data = requests.get(url)
        #print(coin_data.text)
        coin = coin_data.json()
    
    coin_objects = []
    
    #for coin in coins:
        #print(coin)
    temp_coin_obj = Coin(coin['id'], coin['price'])
    temp_coin_obj.timestamp = coin['timestamp']
    temp_coin_obj.one_minute_percentage = float("{:.3f}".format(coin['one_minute_percentage']))
    temp_coin_obj.ten_minute_percentage = float("{:.3f}".format(coin['ten_minute_percentage']))
    temp_coin_obj.thirty_minute_percentage = float("{:.3f}".format(coin['thirty_minute_percentage']))
    temp_coin_obj.one_hour_percentage = float("{:.3f}".format(coin['one_hour_percentage']))
    temp_coin_obj.six_hour_percentage = float("{:.3f}".format(coin['six_hour_percentage']))
    temp_coin_obj.twelve_hour_percentage = float("{:.3f}".format(coin['twelve_hour_percentage']))
    temp_coin_obj.one_day_percentage = float("{:.3f}".format(coin['one_day_percentage']))
    temp_coin_obj.one_week_percentage = float("{:.3f}".format(coin['one_week_percentage']))
    temp_coin_obj.one_month_percentage = float("{:.3f}".format(coin['one_month_percentage']))
    temp_coin_obj.market_cap = float("{:.3f}".format(coin['market_cap']))
    temp_coin_obj.volume = float("{:.3f}".format(coin['volume']))
    temp_coin_obj.currently_bought = False

    coin_objects.append(temp_coin_obj)

    return flask.render_template('coin.html', coins = coin_objects, display=name)

app.run(host='0.0.0.0')

