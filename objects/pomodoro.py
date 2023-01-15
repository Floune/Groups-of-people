import threading
import vlc
import sys
import time

def pomodorof(config, command, radio, chat, tracker, todo, manpage, pomodoro):
		config["mode"] = 6
		if "/start" in command:
			pomodoro.start(10)
		elif command in config["arrows"]:
			config["debug"] = "rfkdsdfksjdfhksjdfh"
			pomodoro.select(command, config)
		elif command == "":
			pomodoro.apply()

class Pomodoro():

	def __init__(self, gui_q):
		self.pomd = 10
		self.pd = 3
		self.duration = self.pomd
		self.gui_q = gui_q
		self.isPaused = True
		self.isPause = False
		self.exitFlag = False
		self.selected = 0
		self.auto = False
		self.timer = threading.Thread(target=self.countdown)
		self.commands = ["Start", "Pause", "Reset", "Autostart"]

	def start(self, duration):
		self.quit()		
		self.exitFlag = False
		self.isPaused = False
		self.timer = threading.Thread(target=self.countdown)
		self.timer.start()
		if self.auto== True:
			self.start(10)
			self.gui_q.put("he")

		
	def countdown(self):
		while self.duration > 0:
			if self.exitFlag == True:
				sys.exit()
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

		self.isPaused = True
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
			self.duration += 60
		if key == "KEY_DOWN" and self.duration > 60:
			self.duration -= 60

	def pause(self):
		self.isPaused = True
		self.exitFlag = True
		self.isPaused = True
		self.gui_q.put("he")

	def quit(self):
		if self.timer.is_alive():
			sys.exit()

	def reset(self):
		if self.timer.is_alive():
			self.exitFlag = True
			self.isPaused = True
			self.isPause = False
			self.duration = self.pomd
			self.gui_q.put("he")

	def apply(self):

		if self.selected == 1:
			self.pause()

		elif self.selected == 0:
			self.start(self.duration)

		elif self.selected == 2:
			self.reset()

		elif self.selected == 3:
			self.auto = not self.auto
			self.gui_q.put("he")



