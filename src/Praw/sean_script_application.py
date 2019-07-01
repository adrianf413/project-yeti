#This is meant to be the more advanced scipt in using PRAW

import praw

reddit = praw.Reddit(client_id ='txRrFGuKPeDnSw',
					client_secret = 'wV7ATmzBZlVnxSok7fIO8FBlyp0',
					udername = 'harkinsean4',
					password = '1508sh1998Red',
					user_agent = 'CCPB v1.0')
					
crypto_subreddit = reddit.subreddit('CryptoCurrency')	#this is the subreddit

hot_crypto = crypto_subreddit.hot(limit = 3)			#this is the retrieves a categroy of that subreddit

for submission in hot_crypto:							#submissions are the subreddit threads, they are an object
	if not submission.stickied:
		print('Title: {}, ups: {}' .format(submission.title, submission.ups))	#title is an attribute of submission
	
		#get the comments on this thread/submission. The .list() is a PRAW functionality
		#it returns a flattened list of all Comments. 
		#This list may contain MoreComments instances if replace_more() was not called first.
		submission.comments.replace_more(limit=0)		
		
		#replace_more is there because in Reddit there are so many replies 
		#to comments that it you must 'load more comments' which is another 
		#call to Reddit database, if this happens we don't bother loading them
		
		comment_list = submission.comments.list()
		
		for comment in comment_list:
			print(20*'-')
			print('Parent ID:', comment.parent())		#this returns in the thread ID, same as submission.id
			print('Comment ID:', comment.id)
			print(comment.body)		#comments are an object, this only prints 'top level comments, no actual replies

			#replies = comment.replies
			#if len(replies) > 0:
			#	for reply in replies:
			#		print('		REPLY: {}' .format(reply.body))
			