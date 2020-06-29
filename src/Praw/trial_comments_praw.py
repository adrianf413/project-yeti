'''
This is a basic script to test out PRAW,
It retrieves the top/hot 3 threads on the r/CryptoCurrency subreddit
it tests out Reddit Comment object attribtues and methods
It looks closely at how .parent() method works 
'''

import praw
import os 
import yaml 

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

    print("signing in")

    reddit = praw.Reddit(client_id=client_id_conf,
                        client_secret=client_secret_conf,
                        username=username_conf,
                        password=password_conf, 
                        user_agent=user_agent_conf)

# Retrive subreddit r/CryptoCurrency
crypto_subreddit = reddit.subreddit('CryptoCurrency')

# this retrieves the hot categroy of that subreddit
hot_crypto = crypto_subreddit.hot(limit=3)

for submission in hot_crypto:

    print("Looping thorugh submissions")

    if not submission.stickied:
        print('Title: {}, ups: {} \n' .format(submission.title, submission.ups))

        submission.comments.replace_more(limit=0)

        print("Try to print the submission object {}".format(submission))
        print("it automatically prints out the ID\n")

        # gets a flattened sit of comments
        comment_list = submission.comments.list()[:101]

        for comment in comment_list:
            print('submission.id : {}' .format(submission.id))
            print('submission : {}' .format(submission))
            print('comment: {}' .format(comment))
            print('comment.id : {}' .format(comment.id))
            print('is comment a top level comment: {}' .format(comment.is_root))
            print('comment.parent: {}' .format(comment.parent))
            print('comment.parent() : {}' .format(comment.parent()))
            print('comment.parent_id : {}' .format(comment.parent_id))
            print('comment.submission: {} \n' .format(comment.submission))

        # comment.parent() returns either a submission object or a comment object
        # depending if a top-level comment called it or a reply comment
        comment_random = comment_list[30]

        comment_random_parent = comment_random.parent()
        print(".parent() method returns type {}".format(type(comment_random.parent())))

        parent_id_string = str(comment.parent())
        print("str(.parent()) returns id which is: {}, type is: {}".format(parent_id_string, type(parent_id_string)))

        try:
            parent_id = comment_random.parent_id
            print(parent_id)

            if parent_id[:2] == 't3':
                print('The parent of this comment is a submission object because the prefix is t3')
            elif parent_id[:2] == 't1':
                print('The parent of this comment is a comment object because the prefix is t1')

        except praw.exceptions.PRAWException as e:
            print(str(e))

        print('end')
