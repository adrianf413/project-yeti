'''
This is the coin class, which will be used to 
store the praw data for the coins

'''

import time
from datetime import datetime
import json


class Coin:
    def __init__(self, id):
        # Creating the attributes of interest for the coins
        self.id = id
        self.classification = "NULL"
        self.confidence = 0
        self.pos_tag_count = 0
        self.neg_tag_count = 0
        self.hits = 0
        self.timestamp = ""

    def update_sentiment(self, classification, confidence):

        if classification == "pos":
            self.pos_tag_count = self.pos_tag_count + 1

        elif classification == "neg":
            self.neg_tag_count = self.neg_tag_count + 1

        self.hits = self.hits + 1

        self.timestamp = datetime.now().strftime("%b-%d-%Y %H-%M-%S")



