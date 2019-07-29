import Reddit_Comments as Comments
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
dictTitle = ''


# This returns the ordered_reddir_comments_dict and prints the thread title
def pop_Thread(conversationDictList):

    dict1 = conversationDictList.pop()

    for key in dict1.keys():
        dictTitle = key
        break
    print(dictTitle)

    return dict1[dictTitle]


# pass in dictionary and it's title, then output dictionary contents to a text file
def convert_Dict_to_Text_File(dictionary, dictTitle):

    textFileName = dictTitle[:10] + '.txt'

    with open(textFileName, 'w+') as myfile:
        myfile.seek(0)

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
    conversationDictList = Comments.return_conversation_dict()

    while conversationDictList:
        dictionary = pop_Thread(conversationDictList)

        textFile = convert_Dict_to_Text_File(dictionary, dictTitle)

        text = replace_contractions("I can't believe you didn't")
        print(text)


if __name__ == '__main__':
    main()
