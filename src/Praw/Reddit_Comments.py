'''
This script takes 3 hot submissions/threads above 50 upvotes,
For each submission it flattens the list of comments 
and organises the comments into a dictionary
    return_conversation_dict : returns an array containing comment dictionaries
'''
import praw
import json
import yaml
import os
from datetime import date
import pickle

coment_dict_List_array = []
conversationDict = {}

def pickle_conv_dict(conv_dict, dictTitle, Conversations_files_location, todays_date):

    textFileName = Conversations_files_location + "/" + todays_date + "_" + dictTitle[:10] + '.pickle'

    conv_dict_f = open(os.path.join(Conversations_files_location, textFileName), "wb")
    pickle.dump(conv_dict, conv_dict_f) 
    conv_dict_f.close()

def write_conv_dict_to_text_file(conv_dict, dictTitle, Conversations_files_location, todays_date):
    """Pass in dictionary and it's title, then output dictionary contents to a text file"""

    textFileName = Conversations_files_location + "/" + todays_date + "_" + dictTitle[:10] + '.txt'

    with open(textFileName, 'w+', encoding='utf8') as myfile:
        
        myfile.seek(0)
        myfile.write(dictTitle)
        myfile.write('\n \n')

    # loop thorugh top level comments
    # conv_dict[comment.id] = [comment.body, comment.ups, {}]
    for comment_id in conv_dict:

        top_level_comment = conv_dict[comment_id][0]
        upvotes = conv_dict[comment_id][1]
        submission_id = conv_dict[comment_id][2]
        replies = conv_dict[comment_id][3]

        with open(textFileName, 'a', encoding='utf8') as my_file:
            my_file.write("'"+top_level_comment + "'," + str(upvotes) + "\n")

        # loop thorugh replies to top level comment 
        for reply_id in replies:  
            with open(textFileName, 'a', encoding='utf8') as my_file:
                
                my_file.write("\t'" + replies[reply_id][0][:100] + "'," + str(replies[reply_id][1]) + "\n")

def return_conversation_dict():
    '''
    this function returns a list of dictionaries made up of: 
    submission titles and their conversation dictionarires
    formatted like: {submission.title: conversationDict}
    '''
    # return coment_dict_List_array - an array of comment dictionaries 
    # for now I only want it to return one dictionary so I'm manipulating the function
    # to return dict_list_1 which is only of size 1
    dict_list_1 = []
    dict_list_1.append(coment_dict_List_array.pop(0))
    return dict_list_1


################################### START ##################################
''' As soon as this script is imported as a module by main.py, all this code below executes'''

# set up the read and write directory
source_dir  = os.path.dirname(os.path.abspath(__file__))

# Get yaml file location
file_name = "configuration.yaml"                            # yaml file contains Reddit account information
yaml_read_location = os.path.join(source_dir, file_name) 

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

    reddit = praw.Reddit(client_id=client_id_conf,
                        client_secret=client_secret_conf,
                        username=username_conf,
                        password=password_conf, 
                        user_agent=user_agent_conf)

else:
    print("Error - could not obtain Reddit account details from yaml configuration file")

# Retrive subreddit r/CryptoCurrency
crypto_subreddit = reddit.subreddit('CryptoCurrency')

# this retrieves the hot categroy of that subreddit
hot_crypto = crypto_subreddit.hot(limit=3)

for submission in hot_crypto:  # submissions are the subreddit threads, they are an object
    if not submission.stickied and submission.ups > 50:  # only take submission if it is not stickied and has > 50 votes

        print('Submission Title: {}, ups: {} \n' .format(submission.title, submission.ups))

        ''' Interacting with the submission object'''

        # replace_more is here because in Reddit there are so many replies
        # to comments that it you must 'load more comments' which is another
        # call to Reddit database, if this happens we don't bother loading them
        submission.comments.replace_more(limit=0)

        # Output all top level comments
        # for top_level_comment in submission.comments:
            # print(top_level_comment.body)

            # Output all replies of the particular top_level_comment            
            # for second_level_comment in top_level_comment.replies:
                #print(second_level_comment.body)

        # gets a flattened list of comments
        # returns a list of comments traversed in a breadth-frst traversal - i.e. flattened comment list ordered by ranked levels
        comment_list = submission.comments.list()[:100]

        # store comments in a dictionary -  must loop through the flattened list
        for comment in comment_list:
            if comment.id not in conversationDict:

                # Check it it is a top level comment
                if comment.is_root is True:

                    # store an array as the value in the conversationDict based on the comment.id key
                    # the array contains 
                    #   index l - top comment's body, 
                    #   index 2 - top comment's upvotes,
                    #   index 4 - top comment's parent thread 
                    #   index 3 - empty dictionary this top comment's replie
                    conversationDict[comment.id] = [comment.body, comment.ups, comment.parent_id, {}]

                # if it is a reply
                # I believe this statement does not differentiate between replies of replies
                if comment.is_root is False:

                    # use comment.parent() to get top comment and get its id to use as key
                    # to find the original top level comment in our dictionary -
                    # fetch the 'value' with this top comment key
                    # which is an array - then specify position 2 -
                    # an empty dictionary is stored in position 2, 
                    # Using the reply's comment.id as the key, 
                    # store an array which contains 
                    #   index 1 - reply comment's body, 
                    #   index 2 - reply comment's ups 

                    # comment.parent() returns parent comment of reply, 
                    parent_of_comment = str(comment.parent()) # surrounding comment.parent() in str() returns id of parent comment is replying to

                    if parent_of_comment in conversationDict:
                        # check if parent of reply comment is a top comment i.e. it exists in conversation dictionary
                        # if true then add it in as a reply to the parent
                        conversationDict[parent_of_comment][3][comment.id] = [comment.body, comment.ups]

                    else:
                        continue
                        # else it must be a reply of a reply
                        # print("Reddit_Comments: Could note get the parent of this comment, I'm guessing it's a reply of a reply")

        # the following code is replicated in main.py in the function convert_Dict_to_Text_File
        # because this code should only return the dictionary not make text files!

        # append the ordered_reddit_comments_dict to a dict with key as title
        coment_dict_List_array.append({submission.title: conversationDict})
    conversationDict = {}  # clear conversationDict for thread submission text file
