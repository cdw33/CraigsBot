from helpers import getCurlResponse
import json

from log import *
log = Logger()

# Archive given link using Wayback Machine; returning archive URL
def getArchiveLinkScrape(url):
	saveURL = "http://web.archive.org/save/"

	data = getCurlResponse(saveURL + url)

	i = data.find("redirUrl") + 13

	archiveURL = "https://web.archive.org/"

	while(not data[i] == '\"'):
		archiveURL += data[i]
		i+=1

	return archiveURL

def getArchiveLinkAPI(url):
	wayback = "http://archive.org/wayback/available?url="

	curl = getCurlResponse(wayback + url)
	
	startAddr = curl.find('url') + 6
	endAddr = startAddr

	while(curl[endAddr] is not ','):
		endAddr += 1
	endAddr -= 1

	archiveURL = curl[startAddr:endAddr]

	log.d(archiveURL)

	return archiveURL