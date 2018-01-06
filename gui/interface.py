# -*- coding: utf-8 -*-
import platform
from gui import tweet
import application
import wx
import buffer
import twitter
import ask
class MainGui(wx.Frame):
	def __init__(self, title):
		self.focused=None
		wx.Frame.__init__(self, None, title=title, size=(350,200)) # initialize the wx frame
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.panel = wx.Panel(self)
		self.main_box = wx.BoxSizer(wx.VERTICAL)
		self.menuBar = wx.MenuBar()
		menu = wx.Menu()
		m_close = menu.Append(-1, "exit", "exit")
		self.Bind(wx.EVT_MENU, self.OnClose, m_close)
		self.menuBar.Append(menu, "&Application")
		menu = wx.Menu()
		m_tweet = menu.Append(-1, "&Tweet", "Tweet")
		self.Bind(wx.EVT_MENU, self.tweet, m_tweet)
		m_reply = menu.Append(-1, "&Reply (Single User)", "Reply")
		self.Bind(wx.EVT_MENU, self.reply, m_reply)
		m_reply_all = menu.Append(-1, "Reply (&All Users)", "ReplyAll")
		self.Bind(wx.EVT_MENU, self.reply_all, m_reply_all)
		m_retweet = menu.Append(-1, "Ret&weet")
		self.Bind(wx.EVT_MENU, self.retweet, m_retweet)
		m_message = menu.Append(-1, "Send &direct message")
		self.Bind(wx.EVT_MENU, self.message, m_message)
		m_like = menu.Append(-1, "Toggle &Like")
		self.Bind(wx.EVT_MENU, self.like, m_like)
		m_quote = menu.Append(-1, "&Quote")
		self.Bind(wx.EVT_MENU, self.quote, m_quote)
		self.menuBar.Append(menu, "&Tweet")
		menu = wx.Menu()
		m_follow = menu.Append(1, "&Follow user", "follow user")
		self.Bind(wx.EVT_MENU, self.follow, m_follow)
		m_unfollow = menu.Append(-1, "&Unfollow user", "unfollow user")
		self.Bind(wx.EVT_MENU, self.unfollow, m_unfollow)
		self.menuBar.Append(menu, "&user")
		self.SetMenuBar(self.menuBar)
		self.list_label=wx.StaticText(self.panel, -1, "Timelines")
		self.list=wx.ListBox(self.panel, -1)
		self.main_box.Add(self.list, 0, wx.ALL, 10)
		self.list.Bind(wx.EVT_LISTBOX, self.on_list_change)
		self.tweets_label=wx.StaticText(self.panel, -1, "Tweets")
		self.tweets=wx.ListBox(self.panel, -1)
		self.main_box.Add(self.tweets, 0, wx.ALL, 10)
		self.tweets.Bind(wx.EVT_BUTTON, self.on_tweets_change)

		accel=[]
		accel.append((wx.ACCEL_CTRL, ord('T'), m_tweet.GetId()))
		accel.append((wx.ACCEL_CTRL, ord('R'), m_reply.GetId()))
		accel.append((wx.ACCEL_CTRL+wx.ACCEL_SHIFT, ord('R'), m_reply_all.GetId()))
		accel.append((wx.ACCEL_CTRL, ord('D'), m_message.GetId()))
		accel.append((wx.ACCEL_CTRL+wx.ACCEL_SHIFT, ord('T'), m_retweet.GetId()))
		if platform.system=="Darwin":
			accel.append((wx.ACCEL_NONE, ord('Q'), m_quote.GetId()))
		else:
			accel.append((wx.ACCEL_CTRL, ord('Q'), m_quote.GetId()))
		accel_tbl=wx.AcceleratorTable(accel)
		self.SetAcceleratorTable(accel_tbl)

		self.panel.Layout()
	def on_list_change(self, event):
		a=self.list.GetString(self.list.GetSelection())
		self.focused=a
		buffer.insert_buffer_items(a)

	def on_tweets_change(self, event):
		dir(event)

	def tweet(self,event):
		t=tweet.TweetGui()
		t.Show()

	def message(self,event):
		f=buffer.get_focused_tweet()
		u=buffer.user(f)
		t=tweet.DMGui(u)
		t.Show()

	def reply(self,event):
		if self.focused=="Direct Messages":
			self.message(0)
		else:
			f=buffer.get_focused_tweet()
			u=buffer.user(f)
			t=tweet.TweetGui("@"+u+" ",f['id_str'])
			t.Show()

	def reply_all(self,event):
		f=buffer.get_focused_tweet()
		u=buffer.get_users_in_tweet(f)
		t=tweet.TweetGui(u+" ",f['id_str'])
		t.Show()

	def like(self,event):
		f=buffer.get_focused_tweet()
		if f['favorited']==True:
			twitter.Unlike(f['id_str'])
		elif f['favorited']==False:
			twitter.Like(f['id_str'])
		stat=twitter.twitter.lookup_status(id=f['id_str'])
		buffer.update_buffer_item(self.focused,self.tweets.GetSelection(),stat[0])

	def follow(self,event):
		t = buffer.get_focused_tweet()
		u = buffer.user(t)
		tw = ask.ask(message="Follow who?",default_value=u) #not works correctly
		print(tw)
		twitter.Follow(tw)

	def unfollow(self, id):
		t = buffer.get_focused_tweet()
		u = buffer.user(t)
		tw = ask.ask(message="Unfollow who?",default_value=u)
		twitter.Unfollow(tw)

	def retweet(self,event):
		f=buffer.get_focused_tweet()
		twitter.Retweet(f['id_str'])

	def quote(self,event):
		f=buffer.get_focused_tweet()
		t=tweet.QuoteGui(f['id_str'])
		t.Show()

	def OnClose(self, event):
		"""App close event handler"""
		self.Destroy()
		twitter.exit()
global window
window=MainGui(application.name+" V"+application.version)
