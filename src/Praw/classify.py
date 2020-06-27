'''

'''

import os
import pickle
from nltk import word_tokenize

# set up the read and write directory
source_dir  = os.path.dirname(os.path.abspath(__file__))

Pickles_read_location = os.path.join(source_dir, "Pickles") 
file_name = "word_features.pickle" 
word_features_f = open(os.path.join(Pickles_read_location, file_name), "rb")
word_features = pickle.load(word_features_f)                                            # UNUSED
word_features_f.close()

Classifier_read_location = os.path.join(source_dir, "Pickles/Classifiers") 
file_name = "voted_classifier.pickle" 
voited_classifier_f = open(os.path.join(Classifier_read_location, file_name), "rb")
voited_classifier = pickle.load(voited_classifier_f) 
voited_classifier_f.close()


def classify(features):

    classification = voited_classifier.classify(features)

    # confidence = voited_classifier.confidence()

    return classification

def find_features(document):
    '''
    - document is a python list of all words in a single Reddit thread
    - word_features is a python list of 5000 most common words/features used in movie reviews
    find_features is responsible for making feature_sets
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
