'''
api_praw.py sets up a REST endpoint to handle PRAW data requests over HTTP  

customers can either request praw data about singular coins or all coins
'''

import flask
from flask import request, jsonify, abort
import json

app = flask.Flask(__name__)
#app.config["DEBUG"] = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route('/api/praw_data', methods=['GET'])
def home():
    return "<h1>Cyrpto Praw history data Home Page</h1><p> you can request about specific coins or all coins</p>"
    # http://localhost:5003/api/praw_data

@app.route('/api/praw_data/history', methods=['GET'])
def return_praw_values():
    if 'name' in request.args:
        name = request.args['name'] # name is the coin we want to GET in HTTP parameter e.g. bitcoin
        
        praw_file = open("prawdata.json", 'r')
        praw_dat = json.load(praw_file)
        #loaded_json  = json.load(coin_file)
        
        for coin_json_dat in praw_dat:
            coin_id = coin_json_dat['id']
            #print(name)
            #print(coin_id)
            if coin_id == name:
                return flask.jsonify(coin_json_dat)
                # http://localhost:5003/api/praw_data/history?name=bitcoin
                
        abort(404)

@app.route('/api/praw_data/history/all', methods=['GET'])
def return_all_praw_values():     
    praw_file = open("prawdata.json", 'r')
    praw_dat = json.load(praw_file)
    return flask.jsonify(praw_dat)

app.run(host='0.0.0.0', port=int(5003)) # gives access thorugh mobile phone