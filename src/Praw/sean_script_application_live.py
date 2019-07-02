'''
This script is meant to take live comments from the
CryptoCurrency subreddit as they come through
'''

import praw
import json

conversationDict = {}

reddit = praw.Reddit(client_id='txRrFGuKPeDnSw',
                     client_secret='wV7ATmzBZlVnxSok7fIO8FBlyp0',
                     udername='harkinsean4',
                     password='1508sh1998Red',
                     user_agent='CCPB v1.0')

crypto_subreddit = reddit.subreddit('CryptoCurrency')  # this is the subreddit

hot_crypto = crypto_subreddit.hot(limit=3)  # this is the retrieves a categroy of that subreddit


# this for loop streams comments from reddit as they come in
# it gets these streamed comments and their parents
# if there is no parent_id, then it must be a top level comment
# we ignore thesae top_level comments by throwing exceptions
for comment in crypto_subreddit.stream.comments():
    try:
        print(30*'_')
        print()
        # API call to get the parent_id
        parent_id = str(comment.parent())
        # if that parent exists, search for the submission/comment using that ID
        # using the reddit object
        submission = reddit.comment(parent_id)
        # If there is no parent, this will throw us an error, which is caught
        print('Parent:')
        print(submission.body)                  # print the parent body
        print('Reply')
        print(comment.body)
    except praw.exceptions.PRAWException as e:
        pass
