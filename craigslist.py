from helpers import getCurlResponse

from log import *
log = Logger()

# Scrape photos links from listing
def getListingPhotos(cl):
	textStartTag = "var imgList ="
	textEndTag = "</figure>"

	startAddr = cl.find(textStartTag)

	#Return if no images found
	if(startAddr == -1):
		return

	startAddr = startAddr+len(textStartTag)+1
	endAddr = cl.find(textEndTag)-14

	#Get raw text between addresses
	rawText = cl[startAddr:endAddr]

	rawLinks = rawText.split(",")
		
	imgLinks = []
	imgLinks = set()

	#Extract images from raw data
	for link in rawLinks:
		if(link.find("url") >= 0):
			imgLinks.add(link[7:len(link)-1])

	return imgLinks

def getListingTitle(cl):
	startTag = "<title>"
	endTag = "</title>"

	startAddr = cl.find(startTag) + len(startTag)
	endAddr = cl.find(endTag)

	title = cl[startAddr:endAddr]

	return title

def getPrice(cl):	
	startTag = "class=\"price\""


	startAddr = cl.find(startTag) + len(startTag) +1

	endAddr = startAddr
	while(cl[endAddr] is not '<'):
		endAddr += 1

	price = cl[startAddr:endAddr]

	return price

def getLocation(cl):
	startTag = "</span><small>"

	startAddr = cl.find(startTag) + len(startTag) + 2

	endAddr = startAddr
	while(cl[endAddr] is not '<'):
		endAddr += 1
	endAddr -= 1

	location = cl[startAddr:endAddr]

	return location	

def getShortDescription(cl):
	startTag = "og:description\" content=\""

	startAddr = cl.find(startTag) + len(startTag)

	endAddr = startAddr
	while(cl[endAddr] is not '<'):
		endAddr += 1
	endAddr -= 3

	desc = cl[startAddr:endAddr]

	return desc	

def getPostDateTime(cl):	
	startTag = "posted: <time datetime=\""

	startAddr = cl.find(startTag) + len(startTag)
	while(cl[startAddr] is not '>'):
		startAddr += 1
	startAddr += 1

	endAddr = startAddr
	while(cl[endAddr] is not '<'):
		endAddr += 1

	dateTime = cl[startAddr:endAddr]

	return dateTime

def getPostDate(cl):
	dateTime = getPostDateTime(cl)

	startAddr = 0
	endAddr = dateTime.find(" ")

	date = dateTime[startAddr:endAddr]

	return date

def getPostTime(cl):
	dateTime = getPostDateTime(cl)

	startAddr = dateTime.find(" ") + 1
	endAddr = len(dateTime)

	time = dateTime[startAddr:endAddr]

	return time

# Ignore certain Craigslist subdomains
def verifyCraigslistUrl(url):
	if(url.find("about") >= 0):
		return 0
	elif(url.find("search") >= 0):
		return 0
	else:		
		return 1

# Scrape item description from listing
def getListingText(cl):
	textStartTag = "<section id=\"postingbody\">"
	textEndTag = "</section>"

	startAddr = cl.find(textStartTag)+len(textStartTag)+1
	endAddr = cl.find(textEndTag)

	rawText = cl[startAddr:endAddr]

	#Cleanup Raw Text
	rawText = rawText.replace('<br>', '')

	print(rawText)

	return

def getListingStatus(cl):
	flagged = "This posting has been flagged for removal"

	if(flagged in cl):
		return "flagged"

