import re
url_re = re.compile(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?]))")
url_re2 = re.compile("(?:\w+://|www\.)[^ ,.?!#%=+][^ ]*")
bad_chars = "'\\.,[](){}:;\""
import gui
class buffer(object):
	def __init__(self,name,statuses):
		self.name=name
		self.statuses=statuses

global buffers
buffers=[]

def insert_buffer_items(name):
	for i in range(len(buffers)):
		if buffers[i].name==name:
			for i2 in range(len(buffers[i].statuses)):
				gui.interface.window.tweets.Insert(process_tweet(buffers[i].statuses[i2]),gui.interface.window.list.GetCount()-1)

def process_tweet(s,return_only_text=False):
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
	template="$user.name$: $text$"
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

	if return_only_text==False:
		return template
	else:
		return text

def find_urls_in_text(text):
	return [s.strip(bad_chars) for s in url_re2.findall(text)]