import threading
import vlc
import sys
import time

def pomodorof(config, command, radio, chat, tracker, todo, manpage, pomodoro):
		config["mode"] = 6
		if "/start" in command:
			pomodoro.start(1500)
		elif command in config["arrows"]:
			config["debug"] = "rfkdsdfksjdfhksjdfh"
			pomodoro.select(command, config)
		elif command == "":
			pomodoro.apply()

class Pomodoro():

	def __init__(self, gui_q):
		self.pomd = 1500
		self.pd = 300
		self.duration = self.pomd
		self.gui_q = gui_q
		self.isPaused = True
		self.isPause = False
		self.selected = 0
		self.commands = ["Start", "Reset"]

	def start(self, duration):
		self.timer = threading.Thread(target=self.countdown)
		self.timer.start()
		
	def countdown(self):
		while self.duration > 0:
			time.sleep(1)
			self.duration -= 1
			self.gui_q.put("qs")
		player = vlc.MediaPlayer("over.mp3")
		player.play()
		time.sleep(6)
		player.release()
		
		if self.isPause == True:
			self.duration = self.pomd
		else :
			self.duration = self.pd
		self.isPause = not self.isPause
		self.gui_q.put("he")
		sys.exit()


	def select(self, key, config):
		if key == "KEY_RIGHT":
			if self.selected < len(self.commands) - 1:
				config["debug"] = "droite"
				self.selected += 1
		if key == "KEY_LEFT":
			if self.selected > 0:
				config["debug"] = "gauche"
				self.selected -= 1
		if key == "KEY_UP" and self.duration < 3600:
			self.duration += 30
		if key == "KEY_DOWN" and self.duration > 30:
			self.duration -= 30

	def apply(self):

		if self.selected == 1:
			self.duration = self.pomd

		elif self.selected == 0:
			self.start(self.duration)


