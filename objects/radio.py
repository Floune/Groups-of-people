import curses
import vlc

class Radio:

	def __init__(self):
		
		self.radios = {
			"Nolife": "https://listen.nolife-radio.com/stream",
			"Culture": "https://stream.radiofrance.fr/franceculture/franceculture_midfi.m3u8?id=radiofrance",
			"NHK": "https://mtist.as.smartstream.ne.jp/30068/livestream/chunklist.m3u8",
			"Algérie": "https://webradio.tda.dz/Adrar_64K.mp3",
			"BBC": "http://stream.live.vc.bbcmedia.co.uk/bbc_radio_one",
			"STOP": "lqlskdjlqkjsd"
		}
		self.currentlyPlaying = "Nothing"
		self.playing = False
		self.selected = 1
		self.instance = vlc.Instance()
		self.player=self.instance.media_player_new()
		self.song = ""

	def updateSelection(self, key):
		if key == "KEY_DOWN" or key == "KEY_RIGHT":
			self.selected += 1
			if self.selected > len(self.radios):
				self.selected = 1

		if key == "KEY_UP" or key == "KEY_LEFT":
			self.selected -= 1
			if self.selected == 0:
				self.selected = len(self.radios)


	def select(self):
		index = self.selected - 1
		self.currentlyPlaying = list(self.radios.keys())[index]
		self.playing = True
		url = list(self.radios.values())[index]
		media=self.instance.media_new(url)
		self.player.set_media(media)
		self.song = "currently offline"
		self.player.play()
		if self.currentlyPlaying == "STOP" and self.playing == True:
			self.currentlyPlaying = "Nothing"
			self.playing = False
			self.player.stop()

	

def radiof(config, command, radio, chat, tracker, todo):	
	config["mode"] = 1

	if command in config["arrows"]:
		config["debug"] = "megaradio" + command
		radio.updateSelection(command)

	elif command == "":
		radio.select()
