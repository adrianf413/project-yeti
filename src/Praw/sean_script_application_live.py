'''
This script is meant to take live comments from the
CryptoCurrency subreddit as they come through
saving us constantly pinging the subreddit,
This script would be enable us to set up alerts,
But we only are allowed 30 API calls / minute
'''
from os import sys
import praw
import os 
import yaml

def main():

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
    crypto_subreddit = reddit.subreddit('CryptoCurrency')  # this is the subreddit

    # this for loop streams comments from reddit as they come in
    # it gets these streamed comments and their parents
    # if there is no parent_id, then it must be a top level comment
    # we ignore these top_level comments by throwing exceptions
    for comment in crypto_subreddit.stream.comments():
        try:
            print(30*'_')
            print()

            # API call to get the parent ID
            parent_id = comment.parent_id

            # if that parent exists, search for the original submission/comment
            # using that ID using

            print('ID is {}'.format(parent_id))

            # if prefix is t3, then the 'parent' is a subreddit thread
            if parent_id[:2] == 't3':
                print('Prefix of parent_id is t3, therefore parent is submission/thread object')

                # print the parent submission title
                print('\nSubmission title: {}\n'.format(comment.submission.title))

            # else if prefix is t1, then the 'parent' is a comment
            elif parent_id[:2] == 't1':

                parentComment = reddit.comment(parent_id[3:])

                print('Prefix of parent_id is t1, therefore parent is comment object')

                print('Belongs to Submission title: {}\n' .format(parentComment.submission.title))
                print('\nParent Comment:')
                print('{}\n'.format(parentComment.body))     # print the parent comment body

            print('Reply:')
            print('{}\n' .format(comment.body))

        except praw.exceptions.PRAWException as e:
            print(str(e))
            pass

        choice = input('Press q to quit or Enter to continue: ')
        if choice == 'q':
            sys.exit(0)
        else:
            main()


if __name__ == '__main__':
    main()
