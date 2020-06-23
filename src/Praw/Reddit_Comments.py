'''
This script takes multiple hot thread above 50 upvotes,
Flattens the list of comments in each thread
Organises the comments into a dictionary
Iterates through the dictionary to make a text file of comments human readable
it can has a function to return list of several dictionaries full of comments for each thread
'''
import praw
import json
import yaml
import os

dict_List = []
dict_list_of_1 = []
conversationDict = {}

def make_a_text_file_for_a_submission(title, ups, id, version):

    textFileName = title[:10] + version + '.txt'

    with open(textFileName, 'w+', encoding='utf8') as myfile:
        myfile.seek(0)

        myfile.write('Made in Reddit_Comments.py ')
        myfile.write('Thread Title: ')
        myfile.write(json.dumps(title))
        myfile.write(json.dumps(ups))
        myfile.write(' ')
        myfile.write(json.dumps(id))

        myfile.write('\n \n')

    return textFileName


def return_conversation_dict():
    '''
    this function returns a list of dictionaries made up of:
    submission titles and their conversation dictionarires
    formatted like: {submission.title: conversationDict}
    '''
    # return dict_List
    # for now I only want it to return one dictionary so I'm manipulating the function
    # to return dict_list_of_1 which is only of size 1
    dict_list_of_1.append(dict_List.pop(0))
    return dict_list_of_1

''' As soon as this script is imported as a module by main.py, all this code below executes'''

# set up the read and write directory
source_dir  = os.path.dirname(os.path.abspath(__file__))

# yaml_dir = os.path.join(source_dir, "..","/") 
# make a write dir if none exists
# if not os.path.exists(read_and_write_dir):
#    os.makedirs(read_and_write_dir)

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

        '''
        uncomment this to make a new text file based off a thread 1/2

        # the following code is replicated in main.py in the function convert_Dict_to_Text_File 1/2
        textFileName = make_a_text_file_for_a_submission(
            submission.title, submission.ups, submission.id, '1')
        '''

        ''' Interacting with the submission object''''

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
                    #   index 3 - empty dictionary this top comment's replie
                    conversationDict[comment.id] = [comment.body, comment.ups, {}]

                # if it is a reply
                # I believe this code does not differentiate between replies of replies
                if comment.is_root is False:

                    # use comment.parent() to get top comment id and use as key
                    # to find the original top level comment -
                    # fetch the 'value'  with this top comment key
                    # which is an array - then specify position 2 -
                    # an empty dictionary is stored in position 2, 
                    # Using the reply's comment.id as the key, 
                    # store an array which contains 
                    #   index 1 - reply comment's body, 
                    #   index 2 - reply comment's ups 

                    parent = str(comment.parent()) # If it is a reply to a comment, it returns the id of the comment it is replying to
                    if parent in conversationDict:
                        # check to make sure the id of comment treply is too is indeed, a top comment
                        conversationDict[parent][2][comment.id] = [comment.body, comment.ups]

        # the following code is replicated in main.py in the function convert_Dict_to_Text_File
        # because this code should only return the dictionary not make text files!

        '''
        uncomment this to make a new text file based off a thread 2/2

        # iterate through each key in dictionary now and write it to a text file 2/2
        for post_id in conversationDict:

            # gets the top level comment body
            tlmessage = conversationDict[post_id][0]
            tlupvotes = conversationDict[post_id][1]

            # get replies of top level comment, replies is a dictionary
            replies = conversationDict[post_id][2]

            with open(textFileName, 'a', encoding='utf8') as my_file:

                my_file.write('{} {}'.format(35*'_', '\nTop Level comment: '))
                my_file.write('{} \nupvotes: {} \n' .format(tlmessage, tlupvotes))

            for reply in replies:  # loop thorugh the keys in replies dictionary

                with open(textFileName, 'a', encoding='utf8') as my_file:

                    my_file.write("\t--\nreply: {} \nupvotes: {}\n" .format(
                        replies[reply][0][:200], replies[reply][1]))
        '''
        # append the ordered_reddit_comments_dict to a dict with key as title
        dict_List.append({submission.title: conversationDict})
    conversationDict = {}  # clear conversationDict for thread submission text file
