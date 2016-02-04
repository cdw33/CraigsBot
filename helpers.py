import re
import pycurl
from StringIO import StringIO

from log import *
log = Logger()

def get_input(string):
	''' Get input from console regardless of python 2 or 3 '''
	try:
		return raw_input(string)
	except:
		return input(string)

def get_config():
	''' Create a config parser for reading INI files '''
	try:
		import ConfigParser
		return ConfigParser.ConfigParser()
	except:
		import configparser
		return configparser.ConfigParser()

# Returns result of cURL-ed url
def getCurlResponse(url):
	buffer = StringIO()

	c = pycurl.Curl()
	c.setopt(c.URL, url)
	# Follow redirect.
	c.setopt(c.FOLLOWLOCATION, True)
	c.setopt(c.WRITEDATA, buffer)
	c.perform()
	c.close()

	return(buffer.getvalue())

# Returns URL extracted from given string
def extractUrlFromString(string):
	url = re.search("(?P<url>https?://[^\s]+)", string).group("url")

	url = url.replace(')', '')
	url = url.replace('\'', '')
	url = url.replace(',', '')

	return url

# Get already processed comments from file
def getCommentIdHistory(set):
	f = open('already_processed', 'r')
	for commentID in f:
		set.add(commentID.replace('\n', ''))	
	f.close()

# Write already processed comments to file
def saveCommentIdHistory(set):
	f = open('already_processed', 'w')
	for commentID in set:
		f.write("%s\n" % commentID)
	f.close()