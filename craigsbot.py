import pycurl
import logging
from reddit import *
from imgur import *
from craigslist import *
from archive import *
from helpers import getCommentIdHistory, saveCommentIdHistory

def initLogging():

	logging.basicConfig(level=logging.INFO)
	logger = logging.getLogger(__name__)

	# create a file handler
	handler = logging.FileHandler('.log')
	handler.setLevel(logging.INFO)

	# create a logging format
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	handler.setFormatter(formatter)

	# add the handlers to the logger
	logger.addHandler(handler)

	return logger


def buildComment(url):
	#comment.reply(' Beep Boop!')
	#archiveURL = getArchiveLink(url)
	#print(archiveURL)
	print(getListingPhotos(url))

# Initialize logging
logger = initLogging()

# Store already processed comments
already_done = set()

# Create client objects
reddit = redditAuth()
imgur = imgurAuth()

# Get comments to process
subreddits = getSubredditList()
mr = reddit.get_subreddit(subreddits)
comments = mr.get_comments(limit=None, threshold=0)

# Read comment history from file
getCommentIdHistory(already_done)

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
saveCommentIdHistory(already_done)