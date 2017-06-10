import gui
def TweetDlg():
	w=gui.tweet.TweetWindow(title="Tweet",parent=gui.interface.window)
	w.display()

def exit_application():
	gui.interface.window.close()