from gui import ask
import collections
import webbrowser
import config
import twython
timelines=collections.OrderedDict()
apikey="3HRxJuiTtakz2plHTqUfPsJkX"
apisecret="ONgUT64zlHevkZXVMy6I1KTlba4iTlCT8LVpY1mQdqd8lYozs0"
def auth():
	global twitter
	config.setup()
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

def Tweet(text):
	twitter.update_status(status=text)
	return True

