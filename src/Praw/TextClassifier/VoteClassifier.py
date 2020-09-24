import nltk
from nltk.classify import ClassifierI
from statistics import mode

class VoteClassifier(ClassifierI):
    '''
    Pass in a list of our classifiers. It inherits from NLTK's ClassifierI
    '''

    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        # Iterate through ALL our classifiers and ask it to classify single test movie review
        # features are all of the words that appear in the movie review and
        # 'features' is a dictionary e.g. -> {'film': True, 'third': False, 'movie': True}
        
        votes = []
        for c in self._classifiers:   # iteratres through ALL classifiers
            v = c.classify(features)  # v is a vote on whether the movie is 'neg' or 'pos'
            votes.append(v)

        # this returns the most common vote, so either most classifier say the movie is 'neg' or 'pos'
        return mode(votes)

    def confidence(self, features):
        # Iterate through all our classifiers and returns a percentage in confidence
        
        votes = []
        for c in self._classifiers:  # iterates through ALL classifiers
            # as before, v is a vote on whether the movie is 'neg' or 'pos'
            v = c.classify(features)
            votes.append(v)

        # votes.count() will count how many 'neg' or 'pos' movie review votes it had from classifiers
        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf
