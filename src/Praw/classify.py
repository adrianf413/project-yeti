'''
This script classify.py encapsulates the functions of the Voted_Classifer and processes a Reddit comment so it is ready to be classified
It will be used by main.py ->(currently being test in main_classify_test.py)

The module does the following does the following
 1. when imported it automatically reads in 
    a. word_features.pickle - 5000 most common words based on training that classifier checks for 
    b. voted_classifier.pickle - the pickled classifer 
 2. 
'''

from TextClassifier.VoteClassifier import VoteClassifier 
import os
import pickle
import sys
from nltk import word_tokenize

# set up the read and write directory
source_dir = os.path.dirname(os.path.abspath(__file__))

# open the pickled word_features file
Pickles_read_location = os.path.join(source_dir, "TextClassifier", "Classifiers") 
file_name = "word_features.pickle" 
word_features_f = open(os.path.join(Pickles_read_location, file_name), "rb")
word_features = pickle.load(word_features_f)                                           
word_features_f.close()

# open the pickled voted_classifier file
Classifier_read_location = os.path.join(source_dir, "TextClassifier", "Classifiers") 
file_name = "Voted_Classifier.pickle" 
voited_classifier_f = open(os.path.join(Classifier_read_location, file_name), "rb")
voited_classifier = pickle.load(voited_classifier_f) 
voited_classifier_f.close()

def classify(features):

    classification = voited_classifier.classify(features)

    return classification

def confidence(features):

    confidence = voited_classifier.confidence(features) # returns a percentae confidence

    return confidence

def find_features(document):
    '''
    - document is a python list of all words in a single moview review
    - word_features is a python list of 5000 most common words/features used in Twitter movie reviews
    find_features is responsible for retruning dictionaries that go into making feature_sets
    the method returns a dictionary containing words as keys with boolean signalling 
    if word in document is one of 5000 most common words
    '''
    words = word_tokenize(document) # most tokensie the document i.e. divide up into singular words
    features = {}

    # word_features is 5000 most common words 

    for w in word_features:
        # loop thorugh word features
        features[w] = (w in words)

    return features # returns dictionary of words present in both document and word features e.g. {'film': True, 'one': False, ...}
