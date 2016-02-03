import re
import pycurl
from StringIO import StringIO

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