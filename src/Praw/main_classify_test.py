'''
This main program gets a list of organised comment dictionaries from Reddit_Comments.py  
that loooks like dict_List = [{submission.title: conversationDict}, ...]

This main program reads from a file a conversation dictionary - vulnerability d.pickle
it tokenise and normalises each comment, then rejoins tokensised words to make comment sentence
Vote Classifer checks what features in comment are present then classifies
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
    """This function prints the submission title and returns the corresponding convDict from the """
    
    dict1 = conversationDictList.pop() # pop the first dictionary element in the list {submission.title: conversationDict}

    # there is only on key in dict1 and it is the submission title
    for key in dict1.keys():
        dictTitle = str(key)
        break

    # use the submission title as the 'key' to return the conversation dictionary
    # formatted like: {submission.title: conversationDict}
    return dictTitle, dict1[dictTitle]


def convert_Dict_to_Text_File(dictionary, dictTitle):
    """Pass in dictionary and it's title, then output dictionary contents to a text file"""
    textFileName = dictTitle[:10] + '.txt'

    with open(textFileName, 'w+', encoding='utf8') as myfile:
        myfile.seek(0)

        myfile.write('Made in main.py ')
        myfile.write('Thread Title: ')
        myfile.write(dictTitle)
        myfile.write('\n \n')

    for post_id in dictionary:

        tlmessage = dictionary[post_id][0]
        tlupvotes = dictionary[post_id][1]
        replies = dictionary[post_id][2]

        with open(textFileName, 'a', encoding='utf8') as my_file:
            # my_file.write('{} {}'.format(35*'_', '\nTop Level comment: '))
            my_file.write('{}'.format('\nTop Level comment: '))
            my_file.write('{} \nupvotes: {} \n' .format(tlmessage, tlupvotes))

        for reply in replies:  # loop thorugh the keys in replies dictionary
            with open(textFileName, 'a', encoding='utf8') as my_file:
                # my_file.write("\t--\nreply: {} \nupvotes: {}\n" .format(
                #    replies[reply][0][:200], replies[reply][1]))
                my_file.write("\t\nreply: {} \nupvotes: {}\n" .format(
                    replies[reply][0][:200], replies[reply][1]))
    return textFileName


def replace_contractions(text):
    """Replace contractions in string of text"""
    return contractions.fix(text)

'''Main reads in a conversation dictionary '''

def main():

    # set up the read and write directory
    source_dir = os.path.dirname(os.path.abspath(__file__))

    textFileName = 'Vulnerability d.pickle'

    # open the pickled convercstion dictionary file
    ConvDict_read_location = os.path.join(source_dir, "TextFiles", "ConversationDictionaries") 
    # file_name = "voted_classifier.pickle" 
    conv_dict_f = open(os.path.join(ConvDict_read_location, textFileName), "rb")
    conv_dict = pickle.load(conv_dict_f) 
    conv_dict_f.close()

    print("Loaded dictionary from file: {}".format(type(conv_dict)))

    # NORMALISATION PROCESS

    i = 0 
    sentiment_set = {} # this is a dictionary containing every single normalised comment

    # contents --> conversationDict[comment.id] = [comment.body, comment.ups, {}]
    for key, entry in conv_dict.items():
        
        #print out first 2 for debugging
        if i < 2:
            print(entry[0]) # entry[0] is comment.body

        # loop through each top level comment in dictionary and nromalise the body

        text = replace_contractions(entry[0])

        # TOKENISATION
        # We tokenise each line of text one at a time
        # return a python array list of words
        words = nltk.word_tokenize(text)
        # print(words)

        # NORMALISATION
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

        if i < 2:
            print(words) # comment.body is now words
            i = i + 1

        comment_body = ' '.join(words) # words are a tokenised list so rejoin as a sentence into comment_body

        sentiment_set[key] = [comment_body, words] # comment_body is a normlasied sentence, words are tokenised as a list

    '''This section of code where will main will call on the classify.py'''

    print("\nCLASSIFICATION\n")

    i = 0
    score = 0
    size = len(sentiment_set)

    for key, entry in sentiment_set.items():
        # loop through each top level comment in dictionary and nromalise the body

        comment_body = entry[0] 
        print(comment_body)                               # print normalsied sentence

        features = Classifer.find_features(comment_body)  # returns a dictionary telling us what 5000 words are present

        if i < 2:
            print("Check comment features: {}".format(features['exists']))
            i = i + 1

        classifcation = Classifer.classify(features)    

        if classifcation == 'neg':
            score = score - 1
        elif classifcation == 'pos':
            score = score + 1

    print("\n\n Thread Score {}\n".format(score))

if __name__ == '__main__':
    main()
