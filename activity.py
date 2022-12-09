from datetime import date, datetime
import time
import json

def trackf(config, command, radio, chat, tracker):
	config["mode"] = 3
	if command[:8] == "/workon ":
		tracker.newActivity(command[8:])

	elif command == "/undo":
		tracker.undo()

	elif command in config["arrows"]:
		tracker.select(command)



class Tracker:
	def __init__(self):
		self.datafile = "track.json"
		self.current = ""
		self.activities = {}
		self.total = []
		self.hasToday = False
		self.today = date.today().strftime("%d-%m-%y")
		self.selectedDay = 0
		self.last = ""
		self.maybeActivity()

	def maybeActivity(self):
		with open(self.datafile, "r") as json_file:
			self.total = json.load(json_file)
			for i, d in enumerate(self.total):
				if d["date"] == self.today:
					self.hasToday = True
					self.selectedDay = i
					self.activities = d["activity"].copy()

	def undo(self):
		if len(self.activities) > 0:
			i = ""
			del self.activities[self.last]
			for k, v in self.activities.items():
				self.current = v
				self.last = k



	def newActivity(self, activity):
		self.current = activity
		start = time.localtime()
		if len(self.activities) < 12:
			self.activities[time.strftime("%H:%M:%S", start)] = activity
			self.last = time.strftime("%H:%M:%S", start)
			if self.hasToday == True:
				for d in self.total:
					if d["date"] == self.today:
						 d["activity"] = self.activities
			else:
				self.total.append({"date":date.today().strftime("%d-%m-%y"), "activity": self.activities})
				self.hasToday = True
			with open(self.datafile, "w") as json_file:				
				json.dump(self.total, json_file)

	def select(self, key):
		if key == "KEY_DOWN" or key == "KEY_RIGHT":
			if self.selectedDay < len(self.total) - 1:
				self.selectedDay += 1
		if key == "KEY_UP" or key == "KEY_LEFT":
			if self.selectedDay > 0:
				self.selectedDay -= 1

	def getActivity(self):
		return self.total