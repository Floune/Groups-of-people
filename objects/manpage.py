import random
import curses

def pagedead(config, command, radio, chat, tracker, todo, manpage, pomodoro):
	config["mode"] = 0
	if command == "KEY_DOWN" or command == "KEY_UP":
		manpage.select(command)
	elif command == "KEY_RIGHT" or command == "KEY_LEFT":
		manpage.changeColor(command)


class Man():
	def __init__(self, config):
		self.selected = 0
		self.lines = [
		{
			"x": 3,
			"y": 3,
			"str": "Radio\t\t\t\t/radio",
			"color": 2
		},
		{
			"x": 3,
			"y": 4,
			"str": "Chat\t\t\t\t\t/chat | /annoy",
			"color": 3
		},
		{
			"x": 3,
			"y": 5,
			"str": "Aide\t\t\t\t\t/help",
			"color": 4
		},
		{
			"x": 3,
			"y": 6,
			"str": "Todo list\t\t\t\t/todo | /todo <tache> | <ENTER> | <SUPPR>",
			"color": 5
		},
		{
			"x": 3,
			"y": 7,
			"str": "Activity tracker\t\t\t/tracker | /workon <project> | /undo",
			"color": 6
		},
		{
			"x": 3,
			"y": 8,
			"str": "Matrix (glitchy)\t\t\t/neo",
			"color": 6
		},
		{
			"x": 3,
			"y": 9,
			"str": "Pomodoro\t\t\t\t/pomodoro",
			"color": 8
		},
	]

	def select(self, key):
		if key == "KEY_DOWN" and self.selected < len(self.lines) - 1:
			self.selected +=1
		elif key == "KEY_UP" and self.selected > 0:
			self.selected -=1

	def changeColor(self, key):
		if key == "KEY_LEFT" and self.lines[self.selected]["color"] > 2:
			self.lines[self.selected]["color"] -=1
		elif key == "KEY_RIGHT" and self.lines[self.selected]["color"] < curses.COLORS - 1:
			self.lines[self.selected]["color"] +=1



			
