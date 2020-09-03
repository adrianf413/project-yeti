'''
This main program takes in conversationDictList from Reddit_Comments.py  
conversationDictList is a python list containing organsied comment dictionaries

Iterates through each dictionary to make a text file of comments human readable
Contractions in the text file are the expanded

INPUT 
conversationDictList --> = [{submission.title: conversationDict}, ...]
    conversationDict --> = conversationDict[comment.id] = [comment.body, comment.ups, repliesDictionary] 
    
'''

from TextClassifier.ClassifierTraining.classifier_sentiment_training import VoteClassifier 
import Reddit_Comments as Reddit_Comments
import classify as Classifer
import contractions
import normalisation
import nltk
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import state_union
import sys
import os
from datetime import date
import pickle

# one time download
# nltk.download('averaged_perceptron_tagger')
# nltk.download('universal_tagset')

tokenisedText = []
tokenisedSent = []
conversationDictList = []
dict1 = {}
dictTitle = 'empty'
textFileList = []

# This returns the ordered_reddit_comments_dict and prints the thread title
def pop_Thread(conversationDictList):
    """Takes in a python list of conversation dictionaries, pops the top one from the list
     and prints the submission title and returns the corresponding conversation dictionary from the """
    
    dict1 = conversationDictList.pop() # pop the first dictionary element in the list {submission.title: conversationDict}

    # there is only on key in dict1 and it is the submission title
    for key in dict1.keys():
        dictTitle = str(key)
        break

    # use the submission title as the 'key' to return the conversation dictionary
    # formatted like: {submission.title: conversationDict}
    return dictTitle, dict1[dictTitle]
                    

def main():

    # set up the read and write directory
    source_dir = os.path.dirname(os.path.abspath(__file__))

    # Location to write Classficiation results to
    Classification_results_location = os.path.join(source_dir, "TextFiles", "ClassificationResults")  

    # Location to write Conversations to
    Conversations_files_location = os.path.join(source_dir, "TextFiles", "ConversationDictionaries")  

    conversationDictList = [] # dicitonary which holds the whole conversation from a Reddit thread
    sentiment_set = {}        # dictionary containing  a python list for each normalised comment and it also in tokensied form -->  {[comment_body, words]..}


    ################## REDDIT COMMENTS ##################

    conversationDictList = Reddit_Comments.return_conversation_dict() # retrieves an array of conversation dictionaries
    conversationDictList = conversationDictList[:1]                   # only want to look at first entry
    #print('length of dict list passed into main: {}' .format(len(conversationDictList)))
    print("We are examining only one conversation dictionary")

    today = date.today()
    todays_date = today.strftime("%b-%d-%Y") # Sep-16-2019

    while conversationDictList:
        print('\n\n'+'loop'+'\n\n')
        dictTitle, conversation_dictionary = pop_Thread(conversationDictList) # pass in array of threads pop first thread in array's conversation dictionary  
        print('Working with: ' + dictTitle)

        today = date.today()
        todays_date = today.strftime("%b-%d-%Y") # Sep-16-2019

        # write the conversation dictionary to a text file
        Reddit_Comments.write_conv_dict_to_text_file(conversation_dictionary, dictTitle, Conversations_files_location, todays_date) # writes the dictionary as a text file

        # Pickle the conversation dicitonary 
        Reddit_Comments.pickle_conv_dict(conversation_dictionary, dictTitle, Conversations_files_location, todays_date) # writes the dictionary as a text file

        ################## NORMALISATION PROCESS ##################

        # conversation_dictionary[comment.id] = [comment.body, comment.ups, {}]
        for key, entry in conversation_dictionary.items():
            # loop through top level comments in dictionary and normalise

            top_level_comment = normalisation.replace_contractions(entry[0]) # only take top level comment
            # upvotes = entry[1]
            submission_id = entry[2]

            ######### TOKENISATION #########
            # returns a python array list of words
            words = nltk.word_tokenize(top_level_comment)
            # print(words)

            ######### NORMALISATION #########
            # remove noun
            words = normalisation.remove_nouns(words) # pass in the tokenised Reddit comment

            # removes non-ascii character such as: emojis, '”',
            words = normalisation.remove_non_ascii(words)

            # Convert all characters to lowercase from list of tokenized words
            words = normalisation.to_lowercase(words)

            # removes punctuation such as: ':' '.' ',' '-' '?' '&' '#' ';' '/' '()' '[]'
            # if it is the middle of a word e.g. ['main.py'] -> ['mainpy']
            words = normalisation.remove_punctuation(words)

            # convert integers representation to text
            # words = normalisation.replace_numbers(words)

            # remove stop words such as:
            words = normalisation.remove_stopwords(words)

            # Stem the words
            # words = normalisation.stem_words(words)
            # print(words)

            # Lem the verbs
            # words = normalisation.lemmatize_verbs(words)
            # print(words)

            # process_sent_content(tokenisedSent) # method is meant to identify NOUN and ADJ but I never used it

            norm_comment_body = ' '.join(words) # words are a tokenised list, so rejoin as a sentence into comment_body

            sentiment_set[key] = [norm_comment_body, entry[0], submission_id] # comment_body is a normlasied sentence, entry[0] is original comment


        ################## CLASSIFICATION OF COVERSATION DICT ##################

        '''This section of code where will main will call on the classify.py'''
        print("\nCLASSIFICATION\n")

        score = 0

        textFileName = Classification_results_location + '/' + dictTitle + "_result.txt"

        with open(textFileName, 'w+', encoding='utf8') as myfile:
            myfile.seek(0)

            # myfile.write('Made in main.py ')
            # myfile.write('\n \n')
            myfile.write("submission_id, comment_id, original_comment_body, norm_comment_body, classification, confidence\n")
    
            for key, entry in sentiment_set.items():
                # find_features for each top level comment in dictionary and classify 

                norm_comment_body = entry[0] 
                original_comment_body = entry[1]
                submission_id = entry[2]

                if not norm_comment_body:

                    print("Normalised comment body: NULL ")
                    myfile.write(submission_id + "," + key + ",'" + original_comment_body + "'," + "NORMALISED AS NULL," + "NULL,NULL" + "\n") # \n")
                    continue                                                    # goes back to top of enclosing loop
                else: 
                    print("Normalised comment body: " + norm_comment_body)           # print normalsied sentence

                features = Classifer.find_features(norm_comment_body)  # returns a dictionary telling us what out of the 5000 words are present
                # --> {'film': True, 'one': False, ...}

                classification = Classifer.classify(features)     # classification result
                confidence = Classifer.confidence(features)       # returns a confidence

                if classification == 'neg':
                    myfile.write(submission_id + "," + key + ",'" + original_comment_body + "'," + norm_comment_body + ",neg," + str(confidence)  + "\n") #\n")
                    score = score - 1
                elif classification == 'pos':
                    myfile.write(submission_id + "," + key + ",'" + original_comment_body + "'," + norm_comment_body + ",pos," + str(confidence)  + "\n") # \n")
                    score = score + 1

        print("\n\n Thread Score {}\n".format(score))
    
if __name__ == '__main__':
    main()
