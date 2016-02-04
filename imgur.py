import time
from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError
from helpers import get_input, get_config, extractUrlFromString, getCurlResponse

from log import *
log = Logger()

class Imgur:

   imgur = None

   client_id = None
   client_secret = None

   def __init__(self):
      config = get_config()
      config.read('auth.ini')
      self.client_id = config.get('imgur', 'client_id')
      self.client_secret = config.get('imgur', 'client_secret')

      self.imgur = ImgurClient(self.client_id, self.client_secret)

   def createAlbum(self, album_title):
   	  log.d('Starting album creation...')

   	  fields = {
	  	'Authorization':'Client-ID {' + self.client_id + '}',
		'title':album_title
	  }  

	  try:
	  	album = self.imgur.create_album(fields)
	  	log.d('Album created successfully.')
	  	return album
	  except ImgurClientError as e:
	  	log.e('Failed to create album, aborting.')
	  	log.e(e.error_message)
	  	log.e(e.status_code)
	  	return None

   def uploadImagesToAlbum(self, album, imgList):
      # For anonymous albums, use album's deletehash instead of id
	  config = {
	  	'album': album['deletehash']
	  }

	  log.d(imgList)

	  #Upload images to album
	  for link in imgList:
	  	log.d('Uploading ' + link + '...')
	  	try:
	  		response = self.imgur.upload_from_url(link, config=config, anon=True)
	  		log.d('Image uploaded successfully.')
	  	except ImgurClientError as e:
	  	    print(e.error_message)
	  	    print(e.status_code)
	  	    log.e("Image upload failed, aborting.")
	  	    return 0  

	  	# Wait for n seconds so Imgur doesn't get upset with us
	  	time.sleep(5)    

	  log.d('All images uploaded successfully.') 

	  return 1    	

   def upload(self, imgLinks, albumName):
	  # Create new Imgur album
	  album = self.createAlbum(albumName)

	  if(album is None):
	  	return None

	  success = self.uploadImagesToAlbum(album, imgLinks)

	  if(not success):
	  	return None
	  
	  # Return album URL
	  albumLink = 'https://imgur.com/a/' + album['id']

	  log.d('Album Link: ' + albumLink)

	  return albumLink

