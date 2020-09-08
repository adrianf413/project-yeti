'''
This main program reads from a file a conversation dictionary - vulnerability d.pickle
it tokenises and normalises each comment, then rejoins tokensised words to make comment sentence
Vote Classifer checks what features in comment are present then classifies

INPUT 
conversationDictList --> = [{submission.title: conv_dict}, ...]
    conv_dict --> = conv_dict[comment.id] = [comment.body, comment.ups, repliesDictionary] 
    
'''

from TextClassifier.ClassifierTraining.classifier_sentiment_training import VoteClassifier 
import classify as Classifer
import contractions
import normalisation
import nltk
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import state_union
import sys
import os
import pickle


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


'''Main reads in a conversation dictionary '''

def main():

    conv_dict = {}       # dicitonary which holds the whole conversation from a Reddit thread
    sentiment_set = {}   # dictionary containing  a python list for each normalised comment and it also in tokensied form -->  {[comment_body, words]..}

    # set up the read and write directory
    source_dir = os.path.dirname(os.path.abspath(__file__))
    textFileName = 'Vulnerability d.pickle'

    # Location to write results to
    Classification_results_location = os.path.join(source_dir, "TextFiles", "ClassificationResults")  

    # open the pickled conversation dictionary file
    ConvDict_read_location = os.path.join(source_dir, "TextFiles", "ConversationDictionaries") 
    conv_dict_f = open(os.path.join(ConvDict_read_location, textFileName), "rb")
    conv_dict = pickle.load(conv_dict_f) 
    conv_dict_f.close()

    print("Loaded dictionary from file: {}".format(type(conv_dict)))

    ################## NORMALISATION PROCESS OF CONVERSATION DICTIONARY ##################

    i = 0 # used to print out first threee comments for debugging

    # conv_dict[comment.id] = [comment.body, comment.ups, {}]
    for key, entry in conv_dict.items():
        # loop through top level comments in dictionary and normalise
        
        #print out first 2 for debugging
        if i <= 4:
            if i == 0: 
                i = i + 1
                continue
            print("\nDEBUGGING comment number: " + str(i))
            print(entry[0]) # entry[0] is comment.body
        

        top_level_comment = normalisation.replace_contractions(entry[0])
        submission_id = top_level_comment.parent_id
        
        ######### TOKENISATION #########
        # returns a python array list of words
        words = nltk.word_tokenize(top_level_comment)
        # print(words)

        ######### NORMALISATION #########
        # remove nouns
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

        norm_comment_body = ' '.join(words) # words are a tokenised list, so rejoin as a sentence into comment_body

        if i <= 4:
            print("\nDEBUGGING comment number: " + str(i) + " post normalisation")
            print(norm_comment_body) # comment.body is now words
            i = i + 1

        sentiment_set[key] = [norm_comment_body, entry[0], submission_id] # comment_body is a normlasied sentence, entry[0] is original comment

    ################## CLASSIFICATION ##################

    '''This section of code where will main will call on the classify.py'''
    print("\nCLASSIFICATION\n")

    i = 0
    score = 0

    textFileName = textFileName[:10] # get conversation dict name without the .pickle

    textFileName = Classification_results_location + '/' + textFileName + "_result.txt"

    with open(textFileName, 'w+', encoding='utf8') as myfile:
        myfile.seek(0)

        # myfile.write('Made in main_classify_test.py ')
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
