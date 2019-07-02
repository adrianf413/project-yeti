'''
This is meant to be the more advanced scipt in using PRAW
It does the same as sean_script.py and also...
if hot thread isn't above 50 upvotes, don't print it
gets rid of 'replace_more' comments
get a flattened sit of comments
make a file called comments.txt
'''
import praw
import json

conversationDict = {}


def make_a_text_file_for_a_submission(title, ups, id, version):

    textFileName = title[:10] + version + '.txt'

    with open(textFileName, 'w+') as myfile:
        myfile.seek(0)

        myfile.write('Thread Title: ')
        myfile.write(json.dumps(title))
        myfile.write(json.dumps(ups))
        myfile.write(' ')
        myfile.write(json.dumps(id))

        myfile.write('\n \n')

    return textFileName


reddit = praw.Reddit(client_id='txRrFGuKPeDnSw',
                     client_secret='wV7ATmzBZlVnxSok7fIO8FBlyp0',
                     udername='harkinsean4',
                     password='1508sh1998Red',
                     user_agent='CCPB v1.0')

crypto_subreddit = reddit.subreddit('CryptoCurrency')  # this is the subreddit

hot_crypto = crypto_subreddit.hot(limit=3)  # this retrieves a categroy of that subreddit

for submission in hot_crypto:  # submissions are the subreddit threads, they are an object
    if not submission.stickied and submission.ups > 50:  # only take submission if it is not stickied and has > 50 votes

        print('Submission Title: {}, ups: {} \n' .format(submission.title, submission.ups))

        textFileName = make_a_text_file_for_a_submission(
            submission.title, submission.ups, submission.id, '1')

        textFileName2 = make_a_text_file_for_a_submission(
            submission.title, submission.ups, submission.id, '2')

        # replace_more is here because in Reddit there are so many replies
        # to comments that it you must 'load more comments' which is another
        # call to Reddit database, if this happens we don't bother loading them
        submission.comments.replace_more(limit=0)

        # gets a flattened list of comments
        comment_list = submission.comments.list()[:100]

        # store comments in a dictionary
        for comment in comment_list:
            if comment.id not in conversationDict:

                # if top level comment
                if comment.is_root is True:

                    # store an array in the conversationDict based on the comment.id key
                    # this array contains the cmment body, upvotes and another dictionary
                    conversationDict[comment.id] = [comment.body, comment.ups, {}]

                    with open(textFileName, 'a') as myfile:

                        myfile.write('Top Level comment: ')
                        myfile.write('{} {} \n' .format(json.dumps(
                            comment.id), json.dumps(comment.body)))

                # if it is a reply
                if comment.is_root is False:

                    # use comment.parent() to get top comment id
                    # and use it as a key to find the original top level
                    # comment - it returns the 'value'  to the key
                    # which is an array - then specify position 1 -
                    # a dictionary is stored in position 1, then using the
                    # reply's comment.id as the key, stored in the value which
                    # is an array of reply ups and its body
                    parent = str(comment.parent())
                    if parent in conversationDict:
                        conversationDict[parent][2][comment.id] = [comment.body, comment.ups]

                    with open(textFileName, 'a') as myfile:

                        myfile.write('{} Reply to parent comment {}: ' .format('\t', parent))
                        myfile.write('{} {} \n' .format(json.dumps(
                            comment.id), json.dumps(comment.body)))

        # iterate through each key in dictionary
        for post_id in conversationDict:

            # gets the top level comment body
            message = conversationDict[post_id][0]

            # get replies, which is dictionary of replies to that top level comment/message
            replies = conversationDict[post_id][2]

            with open(textFileName2, 'a') as my_file:

                my_file.write('{} {}'.format(35*'_', '\nTop Level comment: '))
                my_file.write('{} \n' .format(message))

            for reply in replies:  # loop thorugh the keys in replies dictionary

                with open(textFileName2, 'a') as my_file:

                    my_file.write("\t--\nreply: {} \nupvotes: {}\n" .format(
                        replies[reply][0][:200], replies[reply][1]))

    conversationDict = {}  # clear conversationDict for next text file
