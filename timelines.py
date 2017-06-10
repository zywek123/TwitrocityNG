from gui import interface
from threading import Thread
import buffer
import twitter
class HomeTimeline(object):
	def __init__(self):
		t=Thread(target=self.create_timeline)
		t.start()

	def create_timeline(self):
		self.statuses=twitter.twitter.get_home_timeline(count=200)
		self.buffer=buffer.buffer("Home",self.statuses)
		buffer.buffers.insert(len(buffer.buffers)-1,self.buffer)
		interface.window.list.Insert(buffer.buffers[len(buffer.buffers)-1].name,len(buffer.buffers)-1)

def create():
	h=HomeTimeline()