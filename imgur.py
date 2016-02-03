from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError
from helpers import get_input, get_config, extractUrlFromString

def imgurAuth():
	config = get_config()
	config.read('auth.ini')
	client_id = config.get('imgur', 'client_id')
	client_secret = config.get('imgur', 'client_secret')

	client = ImgurClient(client_id, client_secret)

	# # Authorization flow, pin example (see docs for other auth types)
	# authorization_url = client.get_auth_url('pin')

	# print("Go to the following URL: {0}".format(authorization_url))

	# # Read in the pin, handle Python 2 or 3 here.
	# pin = get_input("Enter pin code: ")

	# # ... redirect user to `authorization_url`, obtain pin (or code or token) ...
	# credentials = client.authorize(pin, 'pin')
	# client.set_user_auth(credentials['access_token'], credentials['refresh_token'])

	# print("Authentication successful! Here are the details:")
	# print("   Access token:  {0}".format(credentials['access_token']))
	# print("   Refresh token: {0}".format(credentials['refresh_token']))

	return client

def makeImgurAlbum(imgLinks):
	#Container to hold imgur links
	imgurLinks = []
	imgurLinks = set()

	print "Starting Imgur album upload."

	for link in imgLinks:
		print("Uploading " + link + "...")
		try:
			response = imgur.upload_from_url(link, config=None, anon=True)
			print("Success!")
		except ImgurClientError as e:
		    print(e.error_message)
		    print(e.status_code)
		    return 0  
  		
		url = extractUrlFromString(str(response))
		imgurLinks.add(url)

	print("Set uploaded successfully!")
	print(imgurLinks)
	return 1		