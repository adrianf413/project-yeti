'''
This main program calls upon Reddit_Comments.py to get list of organised comment dictionaries
Iterates through each dictionary to make a text file of comments human readable
Contractions in the text file are the expanded
'''

import Reddit_Comments as Reddit_Comments
# import re
# import string
# import unicodedata
# import nltk
import contractions
# import inflect
# from bs4 import BeautifulSoup
# from nltk import word_tokenize, sent_tokenize
# from nltk.corpus import stopwords
# from nltk.stem import LancasterStemmer, WordNetLemmatizer

conversationDictList = []
dict1 = {}
dictTitle = 'empty'


# This returns the ordered_reddit_comments_dict and prints the thread title
def pop_Thread(conversationDictList):
    """This function prints the submission title and returns the corresponding convDict from the """

    # pop the first dictionary element in the list
    dict1 = conversationDictList.pop()

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

        message = dictionary[post_id][0]
        replies = dictionary[post_id][2]

        with open(textFileName, 'a', encoding='utf8') as my_file:
            my_file.write('{} {}'.format(35*'_', '\nTop Level comment: '))
            my_file.write('{} \n' .format(message))

        for reply in replies:  # loop thorugh the keys in replies dictionary
            with open(textFileName, 'a', encoding='utf8') as my_file:
                my_file.write("\t--\nreply: {} \nupvotes: {}\n" .format(
                    replies[reply][0][:200], replies[reply][1]))

    return textFileName


def replace_contractions(text):
    """Replace contractions in string of text"""
    return contractions.fix(text)


def main():
    print("\nmain program\n")
    conversationDictList = Reddit_Comments.return_conversation_dict()
    print('length of dict list passed into main: {}' .format(len(conversationDictList)))

    while conversationDictList:
        dictTitle, dictionary = pop_Thread(conversationDictList)
        print('Working with: ' + dictTitle)

        textFile = convert_Dict_to_Text_File(dictionary, dictTitle)

        # read the dictionary converted text file line by line and expand contractions
        with open(textFile, 'r', encoding='utf8') as my_file:
            for line in my_file.readlines():
                text = replace_contractions(line)

                textFileName = textFile + '_contracted_' + '.txt'
                with open(textFileName, 'a', encoding='utf8') as myfile:
                    myfile.write(text)


if __name__ == '__main__':
    main()
