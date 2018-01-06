# -*- coding: utf-8 -*-
import timestring
import datetime
import time
import twitter
import re
import config
url_re = re.compile(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?]))")
url_re2 = re.compile("(?:\w+://|www\.)[^ ,.?!#%=+][^ ]*")
bad_chars = "'\\.,[](){}:;\""
import gui
class buffer(object):
	def __init__(self,name,statuses):
		self.name=name
		self.statuses=statuses
		self.position=0

global buffers
buffers=[]

def get_buffer_item(name,index):
	for i in range(len(buffers)):
		if buffers[i].name==name:
			return buffers[i].statuses[index]

def add_buffer_item(name,item):
	for i in range(len(buffers)):
		if buffers[i].name==name:
			buffers[i].statuses.insert(0,item)
			if gui.interface.window.focused==name:
				gui.interface.window.tweets.Insert(process_tweet(item),0)

def insert_buffer_items(name):
	gui.interface.window.tweets.Clear()
	for i in range(len(buffers)):
		if buffers[i].name==name:
			for i2 in range(len(buffers[i].statuses)):
				gui.interface.window.tweets.Insert(process_tweet(buffers[i].statuses[i2]),gui.interface.window.tweets.GetCount())
			gui.interface.window.tweets.SetSelection(buffers[i].position)

def process_tweet(s,return_only_text=False):
	if s.has_key('full_text')==True:
		text=s['full_text']
	else:
		text=s['text']
	if s.has_key("entities")!=False:
		if s['entities'].has_key("urls")!=False:
			urls=find_urls_in_text(text)
			for url in range(0,len(urls)):
				try:
					text=text.replace(urls[url],s['entities']['urls'][url]['expanded_url'])
				except IndexError:
					pass

	if s.has_key("retweeted_status")!=False:

		qs=s['retweeted_status']
		text="Retweeting "+qs['user']['name']+" ("+qs['user']['screen_name']+": "+process_tweet(qs,True)

	if s.has_key("quoted_status")!=False:

		qs=s['quoted_status']
		urls=find_urls_in_text(text)
		for url in range(0,len(urls)):
			if qs['user']['screen_name'] in urls[url]:

				text=text.replace(urls[url],"Quoting "+qs['user']['name']+": "+process_tweet(qs,True))

	s['text']=text
	if return_only_text==False:
		return template_to_string(s)
	else:
		return text

def find_urls_in_text(text):
	return [s.strip(bad_chars) for s in url_re2.findall(text)]

def template_to_string(s):
	if s.has_key("sender"):
		template=config.appconfig['general']['message_template']
	else:
		template=config.appconfig['general']['tweet_template']

	s['created_at']=parse_date(s['created_at'])
	temp=template.split(" ")
	for i in range(len(temp)):
		if "$" in temp[i]:
			t=temp[i].split("$")
			r=t[1]
			if "." in r:
				q=r.split(".")
				o=q[0]
				p=q[1]

				if s.has_key(o) and s[o].has_key(p):
					try:
						template=template.replace("$"+t[1]+"$",s[o][p])
					except:
						pass

			else:
				if s.has_key(t[1]):
					try:
						template=template.replace("$"+t[1]+"$",s[t[1]])
					except:
						pass
	return template

def get_users_in_tweet(s):
	new=""

	if s.has_key("quoted_status")!=False:
		s['text']+=" "+s['quoted_status']['user']['screen_name']

	if s.has_key("retweeted_status")!=False:
		s['text']+=" "+s['retweeted_status']['user']['screen_name']

	new="@"+s['user']['screen_name']

	weew=s['text'].split(" ")
	for i in range(0,len(weew)):
		if "@" in weew[i] and weew[i]!="@"+twitter.screenname:
			new+=" "+weew[i]
	return new

def user(s):
	if s.has_key('user'):
		return s['user']['screen_name']
	else:
		return s['sender']['screen_name']

def get_focused_tweet():
	index=gui.interface.window.tweets.GetSelection()
	focused=gui.interface.window.focused
	return get_buffer_item(focused,index)

def parse_date(date):
	try:
		ti=datetime.datetime.now()
		tz=time.altzone
		date2=datetime.datetime.strptime(date.replace("+0000 ",""),"%a %b %d %H:%M:%S %Y")
		try:
			date2+=datetime.timedelta(seconds=0-tz)
		except:
			pass
		returnstring=""

		try:
			if date2.year==ti.year:
				if date2.day==ti.day and date2.month==ti.month:
					returnstring=""
				else:
					returnstring=date2.strftime("%m/%d/%Y, ")
			else:
				returnstring=date2.strftime("%m/%d/%Y, ")

			if returnstring!="":
				returnstring+=date2.strftime("%I:%M:%S %p")
			else:
				returnstring=date2.strftime("%I:%M:%S %p")
		except:
			pass
	except:
		return date
	return returnstring

def update_buffer_item(name,index,item):
	remove_buffer_item(name,index)
	insert_buffer_item(name,index,item)

def remove_buffer_item(name,index):
	for i in range(len(buffers)):
		if buffers[i].name==name:
			buffers[i].statuses.pop(index)
			if gui.interface.window.focused==name:
				gui.interface.window.tweets.Delete(index)

def insert_buffer_item(name,index,item):
	for i in range(len(buffers)):
		if buffers[i].name==name:
			buffers[i].statuses.insert(index,item)
			if gui.interface.window.focused==name:
				gui.interface.window.tweets.Insert(process_tweet(item),index)