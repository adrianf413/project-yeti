# This is meant to be the more advanced scipt in using PRAW
# It does the same as sean_script.py and also...
# if hot thread isn't above 50 upvotes, don't print it
# gets rid of 'replace_more' comments
# get a flattened sit of comments
# make a file called comments.txt

import praw
import json

conversationDict = {}

reddit = praw.Reddit(client_id='txRrFGuKPeDnSw',
                     client_secret='wV7ATmzBZlVnxSok7fIO8FBlyp0',
                     udername='harkinsean4',
                     password='1508sh1998Red',
                     user_agent='CCPB v1.0')

crypto_subreddit = reddit.subreddit('CryptoCurrency')  # this is the subreddit

hot_crypto = crypto_subreddit.hot(limit=3)  # this retrieves a categroy of that subreddit

for submission in hot_crypto:  # submissions are the subreddit threads, they are an object
    if not submission.stickied and submission.ups > 50:
        # title is an attribute of submission
        print('Submission Title: {}, ups: {} \n' .format(submission.title, submission.ups))

        with open('comments.txt', 'w+') as myfile:
            myfile.seek(0)

            myfile.write('Thread Title: ')
            myfile.write(json.dumps(submission.title))
            myfile.write(json.dumps(submission.ups))
            myfile.write(' ')
            myfile.write(json.dumps(submission.id))

            myfile.write('\n \n')

        # we want to get the comments on this thread/submission.
        # The .list() is a PRAW functionality
        # It returns a flattened list of all Comments.
        # This list may contain MoreComments instances if replace_more() was not called first.

        submission.comments.replace_more(limit=0)
        # replace_more is there because in Reddit there are so many replies
        # to comments that it you must 'load more comments' which is another
        # call to Reddit database, if this happens we don't bother loading them

        # gets a flattened sit of comments
        comment_list = submission.comments.list()[:100]

        # This is the old way to open a file

        # store comments in a dictionary
        for comment in comment_list:
            if comment.id not in conversationDict:

                # store an array in the conversationDict based on the comment.id key
                # this array contains the comment.body and another dictionary
                conversationDict[comment.id] = [comment.body, {}]

                # if top level comment, store it in the text file
                # if comment.parent() == submission.id:
                if comment.is_root is True:
                    with open('comments.txt', 'a') as myfile:

                        myfile.write('Top Level comment: ')
                        myfile.write('{} {} \n' .format(json.dumps(
                            comment.id), json.dumps(comment.body)))

                # if it is a reply
                if comment.is_root is False:
                        # basically 'if this is not a top level comment' ->
                        # then it must be a reply, therefore use comment.parent()
                        # to get top comment id and use it as a key to find
                        # the original top level comment - it returns the 'value'
                        # to the key which is an array - then specify position 1 -
                        # a dictionary is stored in position 1, then using the
                        # reply's comment.id as the key, stored in the value which
                        # is an array of reply ups and its body
                    parent = str(comment.parent())
                    conversationDict[parent][1][comment.id] = [comment.ups, comment.body]

                    with open('comments.txt', 'a') as myfile:

                        myfile.write('{} Reply to parent comment {}: ' .format('\t', parent))
                        myfile.write('{} {} \n' .format(json.dumps(
                            comment.id), json.dumps(comment.body)))

        # print out the comments from the dictionary
        for post_id in conversationDict:

            message = conversationDict[post_id][0]  # gets the top level comment body
            type(message)
            # replies is a dictionary of replies to the top level comment/message
            replies = conversationDict[post_id][1]
            type(replies)
            if len(replies) > 1:  # if replies dict has more than one array of replies
                print(35*'_')
                print('Original Message: {}'.format(message))

                print('Replies:')
                for reply in replies:  # loop thorugh the keys in replies dictionary
                    print('\t--')
                    # again, limiting to 200 characters for space-saving, not necessary
                    print("\tupvotes: {} \n\treply: {}\n" .format(
                        replies[reply][0], replies[reply][1][:200]))

        # Write the contents of the dictionary to a test file

        # write the contents of the dictionary to a file
        # with open('Crypto_Comments.txt', 'w+') as myfile:
            # myfile.seek(0)
            # myfile.write(json.dumps(conversationDict))
