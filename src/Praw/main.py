'''
This main program gets a list of organised comment dictionaries from Reddit_Comments.py  
that loooks like dict_List = [{submission.title: conversationDict}, ...]
Iterates through each dictionary to make a text file of comments human readable
Contractions in the text file are the expanded
'''

import Reddit_Comments as Reddit_Comments
import contractions
import nltk
from nltk import word_tokenize, sent_tokenize
import normalisation
from nltk.corpus import state_union

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


def process_sent_content(tokenizedSent):
    try:
        for sentence in tokenizedSent:
            # check list contains something
            if sentence:
                tagged = nltk.pos_tag(sentence, tagset='universal')

            # <RB.?> --> '.' means any character and combined with '?' for no more than 0 to 1 characters
            # chunkGram = r"""Chunk: {<RB.?>*<VB.?>*<NNP>+<NN>?}"""
            chunkGram = r"""Chunk: {<ADJ.?>*<ADV.?>*<VERB.?>*<NOUN>+<NOUN>?}"""
            chunkGramNum = r"""Chunk: {<ADJ.?>*<ADV.?>*<VERB.?>*<NOUN>+<NOUN>?<VERB.?>+<NUM.?>?}"""

            '''
            top=ADJ, level=NOUN, comment=NOUN, sometimes upvotes is a VERB or NOUN
            '''

            chunkParser = nltk.RegexpParser(chunkGramNum)
            chunked = chunkParser.parse(tagged)

            print(chunked)
            # chunked.draw()

    except Exception as e:
        print(str(e))


def main():
    print("\nmain program\n")
    # conversationDictList = Reddit_Comments.return_conversation_dict()
    # print('length of dict list passed into main: {}' .format(len(conversationDictList)))

    conversationDictList = ['sample']

    while conversationDictList:
        print('\n\n'+'loop'+'\n\n')
        # dictTitle, dictionary = pop_Thread(conversationDictList)
        # print('Working with: ' + dictTitle)

        # textFile = convert_Dict_to_Text_File(dictionary, dictTitle)
        textFile = 'textFiles/Where shou1.txt'

        # open the text file - then read in all the lines of text, and nromalise each line
        with open(textFile, 'r', encoding='utf8') as my_file:
            for line in my_file.readlines():
                text = replace_contractions(line)

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

                # Stem the words
                # words = normalisation.stem_words(words)
                # print(words)

                # Lem the verbs
                words = normalisation.lemmatize_verbs(words)
                # print(words)

                '''
                For now I want to store two types of tokens -
                a single layered tokenised list
                a double layered tokenised list, sort of for tokenised sentences
                '''
                # tokenisedText is a single layered list of all words, they aren't seperated
                # for word in words:
                # tokenisedText.append(word)

                # tokenisedSent is a double layered list of all sentences, they are seperated
                tokenisedSent.append(words)

                '''
                textFileName = textFile[:10] + '_lemmed_' + '.txt'
                textFileList.append(textFileName)
                with open(textFileName, 'a', encoding='utf8') as myfile:
                    for word in words:
                        myfile.write(word + ' ')
                    myfile.write('\n')
                    # simplejson.dump(words, myfile)
                '''
                # end of text normalisation, normalised text now stored in a text file

        process_sent_content(tokenisedSent)
        
        conversationDictList = [] # empty dictionary so loop ends

    '''This section of code where will main will call on the classify.py'''

    for myfile in textFileList:
        with open(myfile, 'r', encoding='utf8') as myfile:
            print()
                



if __name__ == '__main__':
    main()
