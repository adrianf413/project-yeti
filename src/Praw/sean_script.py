'''
This is a basic script to get used to usign praw,
It retrieves the top/hot 3 threads on the r/CryptoCurrency subreddit
and it prints out these top 3 threads/submission titles
with their number of upvotes
NB: it ignroes the 'sticked' threads on the subreddit
'''

import praw

reddit = praw.Reddit(client_id='txRrFGuKPeDnSw',
                     client_secret='wV7ATmzBZlVnxSok7fIO8FBlyp0',
                     username='harkinsean4',
                     password='1508sh1998Red',
                     user_agent='CCPB v1.0')

crypto_subreddit = reddit.subreddit('CryptoCurrency')
hot_crypto = crypto_subreddit.hot(limit=3)

for submission in hot_crypto:
    if not submission.stickied:
        # print(submission)					#returns the thread id, it is an object
        print('Title: {}, ups: {} \n' .format(submission.title, submission.ups))

        submission.comments.replace_more(limit=0)

        # gets a flattened sit of comments
        comment_list = submission.comments.list()[:5]

        for comment in comment_list:
            print('submission.id : {}' .format(submission.id))
            print('comment.id : {}' .format(comment.id))
            print('is comment a top level comment: {}' .format(comment.is_root))
            print('comment.parent: {}' .format(comment.parent))
            print('comment.parent() : {}' .format(comment.parent()))
            print('parent_id : {}' .format(comment.parent_id))
            print('what submission is comment under: {} \n' .format(comment.submission))
