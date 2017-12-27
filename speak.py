from sys import platform
if platform == "win32":
	from accessible_output2 import outputs
elif platform == "linux" or platform == "linux2":
	import speechd

def speak(text):
	if platform == "win32":
		speaker = outputs.auto.Auto()
		speaker.speak(text)
	elif platform == "linux" or platform == "linux2":
		speaker = speechd.SSIPClient('twitrocity')
		speaker.set_output_module('espeak')
		speaker.set_punctuation(speechd.PunctuationMode.SOME)
		speaker.speak(text)
		speaker.close
