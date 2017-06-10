import config
config.setup()
import twitter
import wx
app = wx.App(redirect=False)
import timelines
from gui import interface
twitter.auth()
interface.window.Show()
timelines.create()
app.MainLoop()