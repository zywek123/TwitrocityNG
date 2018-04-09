import config
from gui import interface
from threading import Thread
import buffer
from twython import TwythonStreamer
import twitter
import sound
snd = twitter.snd
class HomeStream(TwythonStreamer):
	def on_success(self, data):
		if 'text' in data:
			buffer.add_buffer_item("Home",data)
			snd.play("tweet")
		elif 'direct_message' in data:
			buffer.add_buffer_item("Direct Messages",data['direct_message'])
			snd.play("dm")

	def on_error(self, status_code, data):
		print status_code

class MentionsStream(TwythonStreamer):
	def on_success(self, data):
		if 'text' in data:
			if 'recipient' not in data:
				buffer.add_buffer_item("Mentions",data)
				snd.play("reply")

	def on_error(self, status_code, data):
		print status_code

class HomeTimeline(object):
	def __init__(self):
		t=Thread(target=self.create_timeline)
		t.start()
		self.index=0

	def create_timeline(self):
		self.statuses=twitter.twitter.get_home_timeline(count=200,tweet_mode='extended')
		self.buffer=buffer.buffer("Home",self.statuses)
		buffer.buffers.insert(0,self.buffer)
		interface.window.list.Insert(buffer.buffers[0].name,0)
		twitterstream=HomeStream(twitter.apikey, twitter.apisecret,config.appconfig['general']['key'],config.appconfig['general']['secret'])
		twitterstream.user()

class MentionsTimeline(object):
	def __init__(self):
		t=Thread(target=self.create_timeline)
		t.start()
		self.index=0

	def create_timeline(self):
		self.statuses=twitter.twitter.get_mentions_timeline(count=200,tweet_mode='extended')
		self.buffer=buffer.buffer("Mentions",self.statuses)
		buffer.buffers.append(self.buffer)
		interface.window.list.Insert(buffer.buffers[len(buffer.buffers)-1].name,interface.window.list.GetCount())
		twitterstream=MentionsStream(twitter.apikey, twitter.apisecret,config.appconfig['general']['key'],config.appconfig['general']['secret'])
		twitterstream.statuses.filter(track="@"+twitter.screenname)

class LikesTimeline(object):
	def __init__(self):
		t=Thread(target=self.create_timeline)
		t.start()
		self.index=0

	def create_timeline(self):
		self.statuses=twitter.twitter.get_favorites(count=200,tweet_mode='extended')
		self.buffer=buffer.buffer("Likes",self.statuses)
		buffer.buffers.append(self.buffer)
		interface.window.list.Insert(buffer.buffers[len(buffer.buffers)-1].name,interface.window.list.GetCount())

class DirectMessagesTimeline(object):
	def __init__(self):
		t=Thread(target=self.create_timeline)
		t.start()
		self.index=0

	def create_timeline(self):
		self.statuses=twitter.twitter.get_direct_messages(count=200)
		self.buffer=buffer.buffer("Direct Messages",self.statuses)
		buffer.buffers.append(self.buffer)
		interface.window.list.Insert(buffer.buffers[len(buffer.buffers)-1].name,interface.window.list.GetCount())

def create():
	h=HomeTimeline()
	m=MentionsTimeline()
	d=DirectMessagesTimeline()
	l=LikesTimeline()

