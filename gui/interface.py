from gui import tweet
import application
import wx
import buffer
class MainGui(wx.Frame):
	def __init__(self, title):
		self.focused=None
		wx.Frame.__init__(self, None, title=title, size=(350,200)) # initialize the wx frame
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.panel = wx.Panel(self)
		self.main_box = wx.BoxSizer(wx.VERTICAL)
		self.menuBar = wx.MenuBar()
		menu = wx.Menu()
		m_tweet = menu.Append(-1, "&Tweet", "Tweet")
		self.Bind(wx.EVT_MENU, self.tweet, m_tweet)
		self.menuBar.Append(menu, "&Tweet")
		self.SetMenuBar(self.menuBar)
		self.list_label=wx.StaticText(self.panel, -1, "Timelines")
		self.list=wx.ListBox(self.panel, -1)
		self.main_box.Add(self.list, 0, wx.ALL, 10)
		self.list.Bind(wx.EVT_LISTBOX, self.on_list_change)
		self.tweets_label=wx.StaticText(self.panel, -1, "Tweets")
		self.tweets=wx.ListBox(self.panel, -1)
		self.main_box.Add(self.tweets, 0, wx.ALL, 10)
		self.tweets.Bind(wx.EVT_BUTTON, self.on_tweets_change)

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

	def OnClose(self, event):
		"""App close event handler"""
		self.Destroy()
global window
window=MainGui(application.name+" V"+application.version)