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

# Retrive subreddit r/CryptoCurrency
crypto_subreddit = reddit.subreddit('CryptoCurrency')

# this retrieves the hot categroy of that subreddit
hot_crypto = crypto_subreddit.hot(limit=2)

for submission in hot_crypto:
    if not submission.stickied:
        print('Title: {}, ups: {} \n' .format(submission.title, submission.ups))

        submission.comments.replace_more(limit=0)

        # gets a flattened sit of comments
        comment_list = submission.comments.list()[:101]

        for comment in comment_list:
            print('submission.id : {}' .format(submission.id))
            print('comment.id : {}' .format(comment.id))
            print('is comment a top level comment: {}' .format(comment.is_root))
            print('comment.parent: {}' .format(comment.parent))
            print('comment.parent() : {}' .format(comment.parent()))
            print('comment.parent_id : {}' .format(comment.parent_id))
            print('comment.submission: {} \n' .format(comment.submission))

        # comment.parent() returns either a submission object or a comment object
        # depending if a top-level comment called it or a reply comment
        original = comment_list[30].parent()

        print(original)

        try:
            parent_id = original.parent_id
            print(parent_id)

            if parent_id[:2] == 't3':
                print('The parent of this comment is a submission object because the prefix is t3')
            elif parent_id[:2] == 't1':
                print('The parent of this comment is a comment object because the prefix is t1')

        except praw.exceptions.PRAWException as e:
            print(str(e))

        print('end')
