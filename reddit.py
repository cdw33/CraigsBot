import praw
from helpers import get_input, get_config

from log import *
log = Logger()

# Authenticate bot on Reddit
def redditAuth():
	config = get_config()
	config.read('auth.ini')
	uname = config.get('reddit', 'username')
	pw = config.get('reddit', 'password')

	r = praw.Reddit('Craigslist Automated Listing Archiver (CALA) v1.0')
	r.login(uname, pw, disable_warning=True)

	return r

# Get list of subreddits to scan from file
def getSubredditList():
	subreddits = ""

	f = open('subreddits', 'r')
	for sub in f:
		sub = sub.replace('\n', '') #Remove newline chars
		if(subreddits == ""):
			subreddits+= sub
		else:
			subreddits = subreddits + "+" + sub
	f.close()

	return subreddits