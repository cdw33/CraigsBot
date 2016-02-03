from imgur import makeImgurAlbum
from helpers import getCurlResponse

# Scrape photos links from listing
def getListingPhotos(url):
	#<div id="thumbs">
	cl = getCurlResponse(url)

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

	# print(imgLinks)

	# makeImgurAlbum(imgLinks)

	return imgLinks

# Ignore certain Craigslist subdomains
def verifyCraigslistUrl(url):
	if(url.find("about") >= 0):
		return 0
	elif(url.find("search") >= 0):
		return 0
	else:		
		return 1

# Scrape item description from listing
def getListingText(url):
	cl = getCurlResponse(url)

	textStartTag = "<section id=\"postingbody\">"
	textEndTag = "</section>"

	startAddr = cl.find(textStartTag)+len(textStartTag)+1
	endAddr = cl.find(textEndTag)

	rawText = cl[startAddr:endAddr]

	#Cleanup Raw Text
	rawText = rawText.replace('<br>', '')

	print(rawText)

	return

