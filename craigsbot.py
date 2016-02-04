import pycurl
from reddit import *
from imgur import *
from craigslist import *
from archive import *
from helpers import getCommentIdHistory, saveCommentIdHistory

from log import *
log = Logger()

def buildComment(url):
	log.i('Building Comment...')

	# Get Craigslist listing using cURL
	cl = getCurlResponse(url)

	# Get status of listing
	status = getListingStatus(cl)
	if(status is "flagged"):
		log.i('Listing was flagged for removal, ignoring.')
		return

	print(getPostDate(cl))
	print(getPostTime(cl))

	# Retrieve photo links from listing
	log.i('Retrieving listing photos...')
	clPhotos = getListingPhotos(cl)

	# If listing has images, create Imgur album of them
	if(clPhotos is None):
		log.i('Listing has no photos, continuing...')	
	else:
		log.i('Craigslist Photo Links: ')
		log.i(clPhotos)

		# Retrieve photo links from listing
		log.i('Uploading photos to imgur...')
		imgurAlbum = imgur.upload(clPhotos, 'Album Name')
		log.i('Album Link: ')
		log.i(imgurAlbum)

	# Archive listing & retrieve link
	log.i('Retrieving archive link...')
	archiveURL = getArchiveLink(url)
	log.i('Archive Link: ' + archiveURL)	

	archiveURL = str(archiveURL)
	imgurAlbum = str(imgurAlbum)

	# Pretty print final comment to string
	msg = ''
	msg += 'CraigsBot\n\n'
	msg += 'Archived Link: ' + archiveURL + '\n\n'
	msg += 'Listing Text: ' + '' + '\n\n'
	msg += 'Listing Photos: ' + imgurAlbum

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
getCommentIdHistory(already_done)

# Scan comments
for comment in comments:
    if comment.body.find(".craigslist.org") >= 0 and comment.id not in already_done:
        craigsURL = extractUrlFromString(comment.body)

        if craigsURL.find("reddit") == -1 and craigsURL.find("archive") == -1:
        	if(verifyCraigslistUrl(craigsURL)):
        		reply = buildComment(craigsURL)

        		if(reply):
        			log.i('Final Reply Comment:')
        			log.i(reply)
        			# comment.reply(reply)

        		already_done.add(comment.id)

#Write updated comment history to file
saveCommentIdHistory(already_done)