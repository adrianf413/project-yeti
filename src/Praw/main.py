'''
This main program gets a list of organised comment dictionaries from Reddit_Comments.py  
that loooks like dict_List = [{submission.title: conversationDict}, ...]
Iterates through each dictionary to make a text file of comments human readable
Contractions in the text file are the expanded
'''

from ClassifierTraining.sentiment_mod import VoteClassifier
import Reddit_Comments as Reddit_Comments
import classify as Classifer
import contractions
import nltk
from nltk import word_tokenize, sent_tokenize
import normalisation
from nltk.corpus import state_union
import sys
import os
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
    """This function takes in an array of conversation dictionaries, it pops the top one from the list
     and prints the submission title and returns the corresponding convDict from the """
    
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
    textFileName = dictTitle[:15] + '.txt'

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
    conversationDictList = Reddit_Comments.return_conversation_dict() # retrieves an array of conversation dictionaries
    print('length of dict list passed into main: {}' .format(len(conversationDictList)))

    # set up the read and write directory
    source_dir = os.path.dirname(os.path.abspath(__file__))

    conversationDictList = conversationDictList[:1] # only want to look at first entry

    while conversationDictList:
        print('\n\n'+'loop'+'\n\n')
        dictTitle, conversation_dictionary = pop_Thread(conversationDictList) # pass in array of threads pop first thread in array's conversation dictionary  
        print('Working with: ' + dictTitle)

        textFileName = convert_Dict_to_Text_File(conversation_dictionary, dictTitle) # writes the dictionary as a text file

        textFileName = textFileName[:-4] # remove the last 4 characters i.e. '.txt' 
        textFileName = textFileName + '.pickle'

        # save the pickled convercstion dictionary file
        ConvDict_read_location = os.path.join(source_dir, "ConversationDictionaries") 
        # file_name = "voted_classifier.pickle" 
        conv_dict_f = open(os.path.join(ConvDict_read_location, textFileName), "wb")
        pickle.dump(conversation_dictionary, conv_dict_f) 
        conv_dict_f.close()

        sys.exit()

        # open the pickled convercstion dictionary file
        ConvDict_read_location = os.path.join(source_dir, "ConversationDictionaries") 
        # file_name = "voted_classifier.pickle" 
        conv_dict_f = open(os.path.join(ConvDict_read_location, textFileName), "rb")
        conv_dict = pickle.load(conv_dict_f) 
        conv_dict_f.close()

        # NORMALISATION PROCESS

        # conversationDict[comment.id] = [comment.body, comment.ups, {}]
        for key, entry in conversation_dictionary:
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

            # Stem the words
            # words = normalisation.stem_words(words)
            # print(words)

            # Lem the verbs
            # words = normalisation.lemmatize_verbs(words)
            # print(words)

        # process_sent_content(tokenisedSent) # method is meant to identify NOUN and ADJ but I never used it

    '''This section of code where will main will call on the classify.py'''

    print("CLASSIFICATION")

    for key, entry in conversation_dictionary:
        # loop through each top level comment in dictionary and nromalise the body

        comment_body = entry[0] 

        features = find_features(document)

    classifcation = Classifer.classify(features)
    
if __name__ == '__main__':
    main()
