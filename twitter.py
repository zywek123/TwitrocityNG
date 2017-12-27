import os
from gui import ask
import collections
import webbrowser
import config
import twython
timelines=collections.OrderedDict()
apikey="W48NhXLuPeP66yvcXXurhQPY6"
apisecret="jST5JRY7KK8tjyxEm6QcpIWrHrMWeHXqyNPsK5w0ohYd9L7kHu"
#apikey="gRcSncxR8Y2buqPYFd4U8qJKU"
#apisecret="4gq2245Nust9dLCOTzBaJKvJQgrzwiqBYfKVDm7cpw1kb7WfUQ"
def auth():
	global twitter
	twitter = twython.Twython(apikey, apisecret)
	global auth
	if config.appconfig['general']['key']=="" or config.appconfig['general']['secret']=="":
		auth = twitter.get_authentication_tokens()
		OAUTH_TOKEN = auth['oauth_token']
		OAUTH_TOKEN_SECRET = auth['oauth_token_secret']
		webbrowser.open(auth['auth_url'])
		verifier = ask.ask(message='Enter pin:')
		twitter = twython.Twython(apikey, apisecret, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
		tokens=twitter.get_authorized_tokens(verifier)
		config.appconfig['general']['key']=tokens['oauth_token']
		config.appconfig['general']['secret']=tokens['oauth_token_secret']
		config.appconfig.write()

	twitter = twython.Twython(apikey, apisecret,config.appconfig['general']['key'],config.appconfig['general']['secret'])
	account=twitter.get_account_settings()
	global screenname
	screenname=account['screen_name']

def Tweet(text,id=""):
	if id=="":
		twitter.update_status(status=text)
	else:
		twitter.update_status(status=text,in_reply_to_status_id=id)
	return True

def DM(user,text):
	twitter.send_direct_message(user=user,text=text)

def Retweet(id):
	twitter.retweet(id=id)
def Like(id):
	twitter.create_favorite(id=id)

def Unlike(id):
	twitter.destroy_favorite(id=id)

def Quote(text,s):
	url="https://twitter.com/"+s['user']['screen_name']+"/status/"+s['id_str']+"/"
	Tweet(text+" "+url)
def exit():
	os._exit(0)
