# Project Yeti

This is Project Yeti, the joined efforts of Adrian Forde and Sean Harkin
to create CCPB (CryptoCurrencyPredictiveBuying). 

This project will use coinGecko API to download real historical cryptocurrency data
and this, in conjuction with sentiment analysis on cryptocurrency Reddit threads 
will be used to create a trading algorithm. The algorithm's purpose will be to buy 
and sell crypto currencies at the correct time.

There are 3 parts to this project:
1. Coin data service
2. Reddit data service
3. GTS/GTB

The coin data and reddit data parts are exposed to the third part 
(GTS/BTG) as RESTful endpoints which can be queried at any time. All 
three parts are decoupled. 

## CoinGecko API
This project uses the free coin gecko API to retreive information for the crypto currency

## PRAW - Python Reddit API Wrapper
This project uses PRAW to scrape reddit and monitor some crypto subreddits

