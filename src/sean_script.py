# This is a basic script to get used to usign praw

import praw

reddit = praw.Reddit(client_id='txRrFGuKPeDnSw',
                     client_secret='wV7ATmzBZlVnxSok7fIO8FBlyp0',
                     username='harkinsean4',
                     password='1508sh1998Red',
                     user_agent='CCPB v1.0')

crypto_subreddit = reddit.subreddit('CryptoCurrency')

hot_crypto = crypto_subreddit.hot(limit=5)

for submission in hot_crypto:
    if not submission.stickied:
        # print(submission)					#returns the thread id, it is an object
        print('Title: {}, ups: {}' .format(submission.title, submission.ups))
