'''
This script takes multiple hot thread above 50 upvotes,
Flattens the list of comments in each thread
Organises the comments into a dictionary
Iterates through the dictionary to make a text file of comments human readable
it can has a function to return list of several dictionaries full of comments for each thread
'''
import praw
import json

dict_List = []
dict_list_of_1 = []
conversationDict = {}


def make_a_text_file_for_a_submission(title, ups, id, version):

    textFileName = title[:10] + version + '.txt'

    with open(textFileName, 'w+', encoding='utf8') as myfile:
        myfile.seek(0)

        myfile.write('Made in Reddit_Comments.py ')
        myfile.write('Thread Title: ')
        myfile.write(json.dumps(title))
        myfile.write(json.dumps(ups))
        myfile.write(' ')
        myfile.write(json.dumps(id))

        myfile.write('\n \n')

    return textFileName


def return_conversation_dict():
    '''
    this function returns a list of dictionaries made up of:
    submission titles and their conversation dictionarires
    formatted like: {submission.title: conversationDict}
    '''
    # return dict_List
    # for now I only want it to return one dictionary so I'm manipulating the function
    # to return dict_list_of_1 which is only of size 1
    dict_list_of_1.append(dict_List.pop(0))
    return dict_list_of_1


reddit = praw.Reddit(client_id='txRrFGuKPeDnSw',
                     client_secret='wV7ATmzBZlVnxSok7fIO8FBlyp0',
                     udername='harkinsean4',
                     password='1508sh1998Red',
                     user_agent='CCPB v1.0')

# Retrive subreddit r/CryptoCurrency
crypto_subreddit = reddit.subreddit('CryptoCurrency')

# this retrieves the hot categroy of that subreddit
hot_crypto = crypto_subreddit.hot(limit=3)

for submission in hot_crypto:  # submissions are the subreddit threads, they are an object
    if not submission.stickied and submission.ups > 50:  # only take submission if it is not stickied and has > 50 votes

        print('Submission Title: {}, ups: {} \n' .format(submission.title, submission.ups))

        '''
        uncomment this to make a new text file based off a thread 1/2

        # the following code is replicated in main.py in the function convert_Dict_to_Text_File 1/2
        textFileName = make_a_text_file_for_a_submission(
            submission.title, submission.ups, submission.id, '1')
        '''

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
                    # this array contains the tl comment body, upvotes and another dictionary
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

        # the following code is replicated in main.py in the function convert_Dict_to_Text_File
        # because this code should only return the dictionary not make text files!

        '''
        uncomment this to make a new text file based off a thread 2/2

        # iterate through each key in dictionary now and write it to a text file 2/2
        for post_id in conversationDict:

            # gets the top level comment body
            tlmessage = conversationDict[post_id][0]
            tlupvotes = conversationDict[post_id][1]

            # get replies of top level comment, replies is a dictionary
            replies = conversationDict[post_id][2]

            with open(textFileName, 'a', encoding='utf8') as my_file:

                my_file.write('{} {}'.format(35*'_', '\nTop Level comment: '))
                my_file.write('{} \nupvotes: {} \n' .format(tlmessage, tlupvotes))

            for reply in replies:  # loop thorugh the keys in replies dictionary

                with open(textFileName, 'a', encoding='utf8') as my_file:

                    my_file.write("\t--\nreply: {} \nupvotes: {}\n" .format(
                        replies[reply][0][:200], replies[reply][1]))
        '''
        # append the ordered_reddit_comments_dict to a dict with key as title
        dict_List.append({submission.title: conversationDict})
    conversationDict = {}  # clear conversationDict for thread submission text file
