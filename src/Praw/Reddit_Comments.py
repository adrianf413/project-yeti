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

dict_List = []
conversationDict = {}


def make_a_text_file_for_a_submission(title, ups, id, version):

    textFileName = title[:10] + version + '.txt'

    with open(textFileName, 'w+', encoding='utf8') as myfile:
        myfile.seek(0)

        myfile.write('Thread Title: ')
        myfile.write(json.dumps(title))
        myfile.write(json.dumps(ups))
        myfile.write(' ')
        myfile.write(json.dumps(id))

        myfile.write('\n \n')

    return textFileName


def return_conversation_dict():
    return dict_List


reddit = praw.Reddit(client_id='txRrFGuKPeDnSw',
                     client_secret='wV7ATmzBZlVnxSok7fIO8FBlyp0',
                     udername='harkinsean4',
                     password='1508sh1998Red',
                     user_agent='CCPB v1.0')

# Retrive subreddit r/CryptoCurrency
crypto_subreddit = reddit.subreddit('CryptoCurrency')

# this retrieves the hot categroy of that subreddit
hot_crypto = crypto_subreddit.hot(limit=4)

for submission in hot_crypto:  # submissions are the subreddit threads, they are an object
    if not submission.stickied and submission.ups > 50:  # only take submission if it is not stickied and has > 50 votes

        print('Submission Title: {}, ups: {} \n' .format(submission.title, submission.ups))

        textFileName = make_a_text_file_for_a_submission(
            submission.title, submission.ups, submission.id, '1')

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

        # iterate through each key in dictionary
        for post_id in conversationDict:

            # gets the top level comment body
            message = conversationDict[post_id][0]

            # get replies, which is dictionary of replies to that top level comment/message
            replies = conversationDict[post_id][2]

            with open(textFileName, 'a', encoding='utf8') as my_file:

                my_file.write('{} {}'.format(35*'_', '\nTop Level comment: '))
                my_file.write('{} \n' .format(message))

            for reply in replies:  # loop thorugh the keys in replies dictionary

                with open(textFileName, 'a', encoding='utf8') as my_file:

                    my_file.write("\t--\nreply: {} \nupvotes: {}\n" .format(
                        replies[reply][0][:200], replies[reply][1]))

        # append the ordered_reddit_comments_dict to a dict with key as title
        dict_List.append({submission.title: conversationDict})
    conversationDict = {}  # clear conversationDict for thread submission text file
