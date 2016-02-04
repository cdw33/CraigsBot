import pycurl
from reddit import *
from imgur import *
from craigslist import *
from archive import *
from helpers import getCommentIdHistory, saveCommentIdHistory

from log import *
log = Logger()

def processComment(url):

	# Get Craigslist listing using cURL
	cl = getCurlResponse(url)

	# Get status of listing
	status = getListingStatus(cl)
	if(status is "Flagged"):
		return
	elif(status is "PageNotFound"):
		return

	log.i("Found valid comment, gathering data...")	
			
	# Retrieve photo links from listing
	log.i('Retrieving listing photos...')
	clPhotos = getListingPhotos(cl)

	# If listing has images, create Imgur album of them
	imgurAlbum = None
	if(clPhotos is None):
		log.i('Listing has no photos, continuing...')	
	else:
		# Retrieve photo links from listing
		log.i('Uploading photos to imgur...')
		imgurAlbum = imgur.upload(clPhotos, 'Album Name')

	# Get full description from listing
	log.i('Retrieving full description from listing...')
	fullDesc = getListingDescription(cl)

	# Archive listing & retrieve link
	log.i('Retrieving archive link...')
	archiveURL = getArchiveLink(url)

	archiveURL = str(archiveURL)

	return buildReply(archiveURL, fullDesc, imgurAlbum)

def buildReply(archiveURL, fullDesc, imgurAlbum):
	# Pretty print final comment to string
	msg = ''
	msg += 'CraigsBot\n\n'
	msg += '[Archived Listing](' + archiveURL + ')\n\n'

	msg += 'Listing Description:\n`' + fullDesc + '`'

	if(imgurAlbum is not None):
		imgurAlbum = str(imgurAlbum)
		msg += '\n\n[Imgur Album](' + imgurAlbum + ")"

	return msg

# Store already processed comments
already_done = set()

# Create client objects
reddit = redditAuth()
imgur = Imgur()

# Get comments to process
subreddits = getSubredditList()
mr = reddit.get_subreddit(subreddits)
comments = mr.get_comments(limit=None, threshold=0)

# Read comment history from file
#getCommentIdHistory(already_done)

# Scan comments
for comment in comments:
    if comment.body.find(".craigslist.org") >= 0 and comment.id not in already_done:
        craigsURL = extractUrlFromString(comment.body)

        if craigsURL.find("reddit") == -1 and craigsURL.find("archive") == -1:
        	if(verifyCraigslistUrl(craigsURL)):
        		reply = processComment(craigsURL)

        		if(reply):
        			log.i('Reply built, commenting...')
        			#log.i(reply)
        			# comment.reply(reply)
        			log.i("Commenting successful!\n")

        		already_done.add(comment.id)
        		saveCommentIdHistory(already_done) #Write to file to prevent loss

#Write updated comment history to file
saveCommentIdHistory(already_done)