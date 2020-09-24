'''
This  main live program streams live comments from the CryptoCurrency 
subreddit and classifies top level comments from various threads.

Restricted tp 30 API calls / minute

OUTPUT
It writes to two text files
 a. comment details & classification results -> submission_id, comment_id, original_comment_body, norm_comment_body, classification, confidence
 b. all submission theads IDs and title
'''

#from TextClassifier.ClassifierTraining.classifier_sentiment_training import VoteClassifier 
from TextClassifier.VoteClassifier import VoteClassifier 
import Reddit_Comments as Reddit_Comments
from coin import Coin
import classify as Classifer
import normalisation
from datetime import date
from datetime import datetime
import nltk
from os import sys
import praw
import os 
import yaml
import json

coin_praw_objects = []

# List of IDs for the 13 coins that we are starting with 
coin_id_list = ['bitcoin', 'bitcoin-cash', 'ethereum', 'litecoin', 'ripple', 'eos',
                'binancecoin', 'cardano', 'tether', 'stellar','tron', 'cosmos', 
                'dogecoin', 'libra', 'swipe']

def setup_coin_data_file(coin_id_list, jsonFileLocation):
    
    for coin in coin_id_list:

        coin_praw_objects.append(Coin(coin))
     
    json_string = json.dumps([ob.__dict__ for ob in coin_praw_objects]) # method id it is a list
    #print(json_string)

    with open(jsonFileLocation, 'w', encoding='utf8') as myfile:

        myfile.write(json_string)

def set_up_dataset_recording(textFileNameThreads, textFileName):
    
    with open(textFileNameThreads, 'w', encoding='utf8') as myfile:
        myfile.seek(0)

        #myfile.write('Made in scean_script_application_live.py ')
        myfile.write("thread_names, submission_id \n\n")

    with open(textFileName, 'w', encoding='utf8') as myfile:
        myfile.seek(0)

        #myfile.write('Made in scean_script_application_live.py ')
        myfile.write("submission_id, comment_id, original_comment_body, norm_comment_body, classification, confidence, coin_name\n")
        #myfile.write('\n \n')

def main():

    # set up the read and write directory
    source_dir = os.path.dirname(os.path.abspath(__file__))

    # Location to write Classficiation results to
    Classification_results_location = os.path.join(source_dir, "TextFiles", "ClassificationResults")  

    # Location to write Conversations to
    Conversations_files_location = os.path.join(source_dir, "TextFiles", "ConversationDictionaries")  

    sentiment_set = {}                   # dictionary containing  a python list for each normalised comment and it also in tokensied form -->  {[comment_body, words]..}
    threads_names = {}
    subreddit_name = "CryptoCurrency"
    today = date.today()
    todays_date = today.strftime("%b-%d-%Y") # Sep-16-2019
    todays_datetime = datetime.now().strftime("%b-%d-%Y %H-%M")
    textFileNameThreads = Classification_results_location + '/' + todays_datetime + "_" + subreddit_name + "_threads.txt"
    textFileNameResults = Classification_results_location + '/' + todays_datetime + "_" + subreddit_name + "_results.txt"
    jsonFileLocation = source_dir + '/' + "prawdata.json"
    write_count = 0 
    coin_indices = {}
    has_coin_update = False

    coin_indices['bitcoin'] = 0 
    coin_indices['bitcoin-cash'] = 1
    coin_indices['ethereum'] = 2
    coin_indices['litecoin'] = 3 
    coin_indices['ripple'] = 4
    coin_indices['eos'] = 5
    coin_indices['binancecoin'] = 6 
    coin_indices['cardano'] = 7 
    coin_indices['tether'] = 8
    coin_indices['stellar'] = 9
    coin_indices['tron'] = 10
    coin_indices['cosmos'] = 11 
    coin_indices['dogecoin'] = 12 

    setup_coin_data_file(coin_id_list, jsonFileLocation) # Set up PRAW data on coins

    set_up_dataset_recording(textFileNameThreads, textFileNameResults) # Set up textfiles to record results


    ################## SIGN IN TO REDDIT ##################

    file_name = "configuration.yaml" # yaml file contains Reddit account information
    yaml_read_location = os.path.join(source_dir, file_name) # specify where to read and write yaml file from

    with open(yaml_read_location) as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        praw_list = yaml.load(file, Loader=yaml.FullLoader)

        print(praw_list) # prints out a dictionary 

        client_id_conf= praw_list['client_id']
        client_secret_conf= praw_list['client_secret']
        username_conf= praw_list['username']
        password_conf= praw_list['password']
        user_agent_conf= praw_list['user_agent']

    if praw_list != None:

        print("LOGGING:\t signing in")

        reddit = praw.Reddit(client_id=client_id_conf,
                            client_secret=client_secret_conf,
                            username=username_conf,
                            password=password_conf, 
                            user_agent=user_agent_conf)

    # Retrive subreddit r/CryptoCurrency
    crypto_subreddit = reddit.subreddit(subreddit_name)  # this is the subreddit

    # this for loop streams comments from reddit as they come in
    # it gets these streamed comments and their parents
    # if there is no parent_id, then it must be a top level comment
    # we ignore these top_level comments by throwing exceptions
    for comment in crypto_subreddit.stream.comments():
        try:
            print(30*'_')
            is_top_level = False

            parent_id = comment.parent_id # API call to get the parent ID - we do't know if it's a comment or submission id yet 
            comment_id = comment.id
            submission_id = "blank"

            # if prefix of parent_id is t3, then the 'parent' is a subreddit thread
            if parent_id[:2] == 't3':

                if comment_id in sentiment_set:
                    # make sure comment not already in dictionary
                    print("LOGGING:\t top level comment already in sentiment_set")
                    continue

                is_top_level = True

                # print('Prefix of parent_id is t3, therefore parent is submission/thread object')

                print('LOGGING:\t Belongs to Submission title: {}\n' .format(comment.submission.title)) # There are different submissions in the same subreddit
                
                # retrieve some details about the submission
                submission_id = parent_id
                # submission_num_comments = comment.submission.num_comments
                submission_link_flair_text = comment.submission.link_flair_text
                submission_upvotes = comment.submission.score
                #submission_upvote_ratio = comment.submission.upvote_ratio

                if not submission_link_flair_text:
                    # print("LOGGING:\t submission flair "+ submission_link_flair_text)
                    submission_link_flair_text = "NULL"

                # add thread submission id and title to our dictionary 
                if submission_id not in threads_names:
                    threads_names[submission_id] = comment.submission.title

                    with open(textFileNameThreads, 'a', encoding='utf8') as myfile:

                        myfile.write("" + submission_id + "," + threads_names[submission_id] + "," + str(submission_upvotes) + "," + submission_link_flair_text + "\n")

                
            # else if prefix of parent is t1, then this is a reply comment
            elif parent_id[:2] == 't1':
                # print("Prefix of parent_id is t1, therefore the comment's parent is a comment object\n")

                if parent_id in sentiment_set:
                    # check if parent comment of this reply is in sentiment set
                    # if it is, add it, this was we now ONLY have top level comments & comments sub top level 

                    submission_id = comment.link_id # submission id which comment belongs to 

                    if comment_id in sentiment_set:
                        # make sure comment not already in dictionary
                        print("LOGGING:\t reply level comment already in sentiment_set")
                        continue


                    print('LOGGING:\t Reply comment belongs to comment id : {}\n' .format(parent_id)) # There are different submissions in the same subreddit
                    # print('LOGGING:\t Belongs to Submission title: {}\n' .format(comment.submission.title)) # There are different submissions in the same subreddit
                
                else:
                    # if comment's parent not in sentiment set continue
                    continue

                # details about this reply comment's parent
                # parentComment = reddit.comment(parent_id[3:]) # find original parent comment
                # print('Belongs to Submission title: {}\n' .format(parentComment.submission.title))
                # print('\nParent Comment:')
                # print('{}\n'.format(parentComment.body))     # print the parent comment body


            print('__Comment Under Analysis__:')
            print('{}\n' .format(comment.body))

         # close the try statement for streaming comments 

        except praw.exceptions.PRAWException as e:
            print(str(e))
            continue
            # pass


        ################## NORMALISATION PROCESS ##################

        top_level_comment = normalisation.replace_contractions(comment.body)
        coin_name = "NULL"

        if "I am a bot" in top_level_comment:
            print("LOGGING:\t Ignore bot comment")
            continue
            # make sure coment is not a bot moderator 

        ######### TOKENISATION #########
        # returns a python array list of words
        words = nltk.word_tokenize(top_level_comment)
        # print(words)

        # look for coin names
        coin_comment = normalisation.find_coin(words)               # pass in the tokenised Reddit comment

        if coin_comment:
            # check is list contains anything 
            mode_coin= max(coin_comment, key=coin_comment.count)   # get mode of coin names found - note it has quadratic run time but small list anyway
        else:
            # if the normalised comment doesn't mention a coin just continue
            print("LOGGING:\t No Coin mentioned in comment, continue and retrieve new comment")
            continue

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

        if words:
            # if tokenised list contains words, rejoin as a sentence into comment_body
            norm_comment_body = ' '.join(words) 
        else:
            norm_comment_body = "" # else leave norm_comment_body empty, a blank string e.g. "" is falsy
        
        is_classifed = False

        # boolean is_top_level could be added to sentiment_set
        sentiment_set[comment_id] = [norm_comment_body, comment.body, submission_id, is_classifed, mode_coin] # comment_body is a normlasied sentence, entry[0] is original comment

        ################## CLASSIFICATION OF COMMENT ##################

        for key, entry in sentiment_set.items():
            # find_features for each top level comment in dictionary and classify 
            print("LOGGING:\t start of sentiment_set loop") 

            norm_comment_body = entry[0]
            original_comment_body = entry[1].replace("\n", " ") # get rid of the new lines and replace with a space
            submission_id = entry[2]
            coin_name = entry[4]

            if not entry[3]:
                # if is_classified is Flase, continue

                is_classifed = True                     # is_classified morfe represent is_analysed, norm_comment_body may be null
                sentiment_set[key][3] = is_classifed

                if norm_comment_body:
                    # check to if the normalised comment has retained any words - no point analysing comment if empty

                    #if coin_name != "NULL":
                        # was gonna put this in but if normalisation.find_coin comes up empty handed the comment is skipped anyway

                    features = Classifer.find_features(norm_comment_body)  # returns a dictionary telling us what out of the 5000 words are present, may or may not be empty
                    # --> {'film': True, 'one': False, ...}

                    classification = Classifer.classify(features)     # classification result
                    confidence = Classifer.confidence(features)       # returns a confidence

                    index_in_list = coin_indices[coin_name]
                    coin_praw_objects[index_in_list].update_sentiment(classification, confidence) # update the coin praw object attirbute

                    has_coin_update = True
                                    
                else:
                    # norm_comment_body empty so we can't classify it
                    print("LOGGING:\t norm_comment_body is empty") 
                    classification = "NULL"
                    confidence = "NULL"

            else:
                # has already been classified -  continue and don't write to text file
                print("LOGGING:\t normalised comment has already been classified") 
                continue 

            ############## Writing Result To Text File ##############
            
            with open(textFileNameResults, 'a', encoding='utf8') as myfile:

                print("LOGGING:\t writing to text file") 

                if classification == "NULL":
                    
                    print("Normalised comment body: NULL ")
                    myfile.write(submission_id + "," + key + ",'" + original_comment_body + "'," + "NORMALISED AS NULL," + "NULL,NULL" + "\n") # \n")
                                                                                    
                else: 
                    print("Normalised comment body: " + norm_comment_body)           # print normalsied sentence

                if classification == 'neg':
                    myfile.write(submission_id + "," + key + ",'" + original_comment_body + "'," + norm_comment_body + ",neg," + str(confidence) + "," + coin_name + "\n") #\n")
                elif classification == 'pos':
                    myfile.write(submission_id + "," + key + ",'" + original_comment_body + "'," + norm_comment_body + ",pos," + str(confidence) + "," + coin_name + "\n") # \n")

        
        ################## CLOSE CLASSIFICATION - UPDATE COIN PRAW DATA ##################

        if has_coin_update:

            print("LOGGING:\t has coin update, continue")

            with open(jsonFileLocation, 'w', encoding='utf8') as myfile:
                
                json_string = json.dumps([ob.__dict__ for ob in coin_praw_objects]) # method id it is a list
                #print(json_string)
                myfile.write(json_string)

                write_count = write_count + 1

            has_coin_update = False
        
        else:
            print("LOGGING:\t No coin update, continue")


        '''
        choice = input('Press q to quit or Enter to continue: ')
        if choice == 'q':
            sys.exit(0)
        else:
            main()
        '''

if __name__ == '__main__':
    main()
