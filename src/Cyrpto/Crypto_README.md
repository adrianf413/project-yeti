# Service for all data relating to Cryptocurrency data #

This service consists of 2 microservices working together. The first service is used to continuously store and update the data for each coin, and then store this information in a file, and the other service exposes this data in the file using a REST API for use in another serive of project yeti.

## Data Retreival and Storage ##
Consists of 2 python modules, Application.py and recent_history.py. Uses the coingecko REST API to query the price information of all coins. 

Application.py 
1. first create the file to store the data if it does not already exist.
2. instantiate the recent_history helper module which is used to collect and update the price every minute 
3. Update the file with new coin information every minute
4. Loop through the update every minute continuously

recent_history.py - helper class for application.py
1. Once instantiated, it will create a list of coin objects to store the price of each coin for every minute of a 24 hour cycle.
2. Contains a method to update the object in the list with the time stamp relating to the current time
3. contains method(s) to get the percentage increases/decreases for each coin based on the current price against the data it has collected

## REST API ##
_______.py (not named yet)

Uses python Flask to expose the coin data in the file as a REST API, acessible to anything on the same network. 

Example usage:

request: http://127.0.0.1:5001/coin_data/history?name=bitcoin

response: 
{
  "currently_bought": "false", 
  "id": "dogecoin", 
  "one_day_percentage": 0, 
  "one_hour_percentage": 0, 
  "one_minute_percentage": 0, 
  "one_month_percentage": 0, 
  "one_week_percentage": 0, 
  "price": 0.00279212, 
  "six_hour_percentage": 0, 
  "ten_minute_percentage": 0, 
  "thirty_minute_percentage": 0, 
  "timestamp": 0, 
  "twelve_hour_percentage": 0
}

## Docker Container

This service will be running on a docker container on the same network as the rest of project yeti, with port 5001 exposed. 