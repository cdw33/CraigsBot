from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError
from helpers import get_input, get_config, extractUrlFromString, getCurlResponse

from log import *
log = Logger()

class Imgur:

   imgur = None

   def __init__(self):
      config = get_config()
      config.read('auth.ini')
      client_id = config.get('imgur', 'client_id')
      client_secret = config.get('imgur', 'client_secret')

      self.imgur = ImgurClient(client_id, client_secret)

   def createAlbum(self, album_title):
   	  log.i('Starting album creation...')

   	  fields = {
	  	'Authorization':'Client-ID {a76fcf734951688}',
		'title':album_title
	  }  

	  try:
	  	album = self.imgur.create_album(fields)
	  	log.i('Album created successfully.')
	  	return album
	  except ImgurClientError as e:
	  	log.e('Failed to create album, aborting.')
	  	log.e(e.error_message)
	  	log.e(e.status_code)

   def uploadImagesToAlbum(self, album, imgList):
      # For anonymous albums, use album's deletehash instead of id
	  config = {
	  	'album': album['deletehash']
	  }

	  #Upload images to album
	  for link in imgList:
	  	log.i('Uploading ' + link + '...')
	  	try:
	  		response = self.imgur.upload_from_url(link, config=config, anon=True)
	  		log.i('Success!')
	  	except ImgurClientError as e:
	  	    print(e.error_message)
	  	    print(e.status_code)
	  	    return 0  

	  	log.i('All images uploaded successfully.') 
	  	return 1    	

   def upload(self, imgLinks, albumName):
	  # Create new Imgur album
	  album = self.createAlbum(albumName)

	  success = self.uploadImagesToAlbum(album, imgLinks)

	  if(not success):
	  	return None
	  
	  # Return album URL
	  albumLink = 'https://imgur.com/a/' + album['id']
	  return albumLink

