# This is meant to be the more advanced scipt in using PRAW

import praw
conversationDict = {}

reddit = praw.Reddit(client_id='txRrFGuKPeDnSw',
                     client_secret='wV7ATmzBZlVnxSok7fIO8FBlyp0',
                     udername='harkinsean4',
                     password='1508sh1998Red',
                     user_agent='CCPB v1.0')

crypto_subreddit = reddit.subreddit('CryptoCurrency')  # this is the subreddit

hot_crypto = crypto_subreddit.hot(limit=5)  # this is the retrieves a categroy of that subreddit

for submission in hot_crypto:  # submissions are the subreddit threads, they are an object
    if not submission.stickied and submission.ups > 500:
        # title is an attribute of submission
        print('Submission Title: {}, ups: {}' .format(submission.title, submission.ups))

        # we want to get the comments on this thread/submission.
        # The .list() is a PRAW functionality
        # It returns a flattened list of all Comments.
        # This list may contain MoreComments instances if replace_more() was not called first.

        submission.comments.replace_more(limit=0)
        # replace_more is there because in Reddit there are so many replies
        # to comments that it you must 'load more comments' which is another
        # call to Reddit database, if this happens we don't bother loading them

        comment_list = submission.comments.list()[:100]

        for comment in comment_list:
            if comment not in conversationDict:
                # store an array in the conversationDict based on the comment.id key
                # this array contains the comment.body and another dictionary
                conversationDict[comment.id] = [comment.body, {}]
                if comment.parent() != submission.id:  # basically 'if this is not a top level comment' ->
                    # then it must be a reply, therefore get the originanl comment parent id () as a string and
                    # find the exisiting id of the top level comment
                    # place the comment.id in position 1 of the array which is a nestedd conversationDict
                    # and the value to that key is the comment ups and comment body
                    parent = str(comment.parent())
                    conversationDict[parent][1][comment.id] = [comment.ups, comment.body]

        print('Done sorting comments')
        print(20*'*')

        for post_id in conversationDict:
            message = conversationDict[post_id][0]  # gets the top level comment body
            type(message)
            # replies is a dictionary of replies to the comment/message
            replies = conversationDict[post_id][1]
            type(replies)
            if len(replies) > 1:  # if replies has more than one array of replies
                print(35*'_')
                print('Original Message: {}'.format(message))

                print('Replies:')
                for reply in replies:  # loop thorugh the keys in replies dictionary
                    print('\t--')
                    # again, limiting to 200 characters for space-saving, not necessary
                    print("\tupvotes: {} \n\treply: {}\n" .format(
                        replies[reply][0], replies[reply][1][:200]))
