import pycurl
import time
import praw
from reddit import *
from imgur import *
from craigslist import *
from archive import *
from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError

# Get already processed comments from file
def getCommentIdHistory():
	f = open('already_processed', 'r')
	for commentID in f:
		already_done.add(commentID)	
	f.close()

# Write already processed comments to file
def saveCommentIdHistory():
	f = open('already_processed', 'w')
	for commentID in already_done:
		f.write("%s\n" % comment.id)
	f.close()

def buildComment(url):
	#comment.reply(' Beep Boop!')
	#archiveURL = getArchiveLink(url)
	#print(archiveURL)
	print(getListingPhotos(url))

# Store already processed comments
already_done = []
already_done = set()

# Create client objects
reddit = redditAuth()
imgur = imgurAuth()

# Get comments to process
subreddits = getSubredditList()
mr = reddit.get_subreddit(subreddits)
comments = mr.get_comments(limit=None, threshold=0)

# Read comment history from file
getCommentIdHistory()	

# Scan comments
for comment in comments:
    if comment.body.find(".craigslist.org") >= 0 and comment.id not in already_done:
        craigsURL = extractUrlFromString(comment.body)

        if craigsURL.find("reddit") == -1 and craigsURL.find("archive") == -1:
        	if(verifyCraigslistUrl(craigsURL)):
        		# reply = buildComment()
        		# comment.reply(reply)
        		buildComment(craigsURL)	        		
        		already_done.add(comment.id)

#Write updated comment history to file
saveCommentIdHistory()