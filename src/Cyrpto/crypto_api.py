import flask
from flask import request, jsonify, abort
import json


app = flask.Flask(__name__)
#app.config["DEBUG"] = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route('/coin_data', methods=['GET'])
def home():
    return "<h1>Cyrpto Coin history data Home Page</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/coin_data/history', methods=['GET'])
def return_coin_values():
    if 'name' in request.args:
        name = request.args['name']
        
        coin_file = open("12hourstorage.json", 'r')
        coin_dat = json.load(coin_file)
        #loaded_json  = json.load(coin_file)
        for x in coin_dat:
            coin_id = x['id']
            print(name)
            print(coin_id)
            if coin_id == name:
                return flask.jsonify(x)
        abort(404)

@app.route('/coin_data/history/all', methods=['GET'])
def return_all_coin_values():     
    coin_file = open("12hourstorage.json", 'r')
    coin_dat = json.load(coin_file)
    return flask.jsonify(coin_dat)

app.run(host='0.0.0.0', port=int(5001))

