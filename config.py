# -*- coding: utf-8 -*-
import config_utils
from sys import platform
import os
import shutil
if platform == "win32":
	user = os.getenv('AppData')
	if os.path.exists("config.cfg"):
		if not os.path.exists(user+"\\twitrocity"):
			os.makedirs(user+"\\twitrocity")
		shutil.move("config.cfg", user+"\\twitrocity\\twitrocity.cfg")
	else:
		if not os.path.exists(user+"\\twitrocity"):
			os.makedirs(user+"\\twitrocity")
	MAINFILE = user+"\\twitrocity\\twitrocity.cfg"
elif platform == "linux" or platform == "linux2":
	user = os.getenv("user")
	if os.path.exists("/home/"+user+"/.config/twitrocity.cfg"):
		if not os.path.exists("/home/"+user+"/.twitrocity"):
			os.makedirs("/home/"+user+"/.twitrocity")
		shutil.move("/home/"+user+"/.config/twitrocity.cfg", "/home/"+user+"/.twitrocity/twitrocity.cfg")
	else:
		os.makedirs("/home/"+user+"/.twitrocity")
	MAINFILE = "/home/"+user+"/.silver/twitrocity.cfg"
MAINSPEC = "app.defaults"
#appconfig=None
def setup():
	global appconfig
	appconfig = config_utils.load_config(MAINFILE, MAINSPEC)
