from helpers import getCurlResponse

from log import *
log = Logger()

# Archive given link using Wayback Machine; returning archive URL
def getArchiveLink(url):
	saveURL = "http://web.archive.org/save/"

	data = getCurlResponse(saveURL + url)

	i = data.find("redirUrl") + 13

	archiveURL = "https://web.archive.org/"

	while(not data[i] == '\"'):
		archiveURL += data[i]
		i+=1

	return archiveURL