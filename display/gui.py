import curses
from datetime import date, datetime
from display.matrix import rain
import threading
import math
from display.matrix import rain


def gui(config, gui_q, txtBox, toolBox, mainBox, radio, chat, tracker, todo, manpage, pomodoro):
	command = ""
	i=1

	while command != "/quit":
		tools(toolBox, config, chat)
		command = gui_q.get()
		main(mainBox, config, radio, chat, tracker, todo, manpage, pomodoro)
		# if command:
		# 	mainBox.addstr(i, 2, str(command))
		# 	i+=1
		mainBox.box()
		mainBox.refresh()
		txtBox.clear()
		txtBox.box()
		txtBox.refresh()


def tools(toolBox, config, chat):
	toolBox.clear()
	title = config["modes"][config["mode"]]["title"]
	margin = int(curses.COLS / 2 - len(title) / 2)
	toolBox.addstr(2, margin, title)
	toolBox.addstr(2, 2, config["debug"])
	if config["mode"] == 2:
		toolBox.addstr(3, 2, "<", curses.color_pair(1)) 
		if chat.selectedConnectedUser == -1:
			toolBox.addstr(3, 4, "{} {}".format(len(chat.connected), "utilisateurs connectés" if len(chat.connected) > 1 else "utilisateur connecté"))
			toolBox.addstr(3, 29, ">", curses.color_pair(1)) 

		elif chat.selectedConnectedUser >= 0 and chat.selectedConnectedUser < len(chat.connected):
			toolBox.addstr(3, 4, "{}".format(chat.connected[chat.selectedConnectedUser]), curses.color_pair((chat.connected.index(chat.connected[chat.selectedConnectedUser]) + 4)))
			toolBox.addstr(3, 5 + len(chat.connected[chat.selectedConnectedUser]), ">", curses.color_pair(1)) 
		toolBox.addstr(4, 2, "(notifications activées)" if config["annoy"] == True else "(notifications désactivées)")

	toolBox.box()
	toolBox.refresh()

def main(mainBox, config, radio, chat, tracker, todo, manpage, pomodoro):
	if config["mode"] == 0:
		help(config, mainBox, manpage)
		
	elif config["mode"] == 1:
		wtf = {}
		mainBox.clear()
		mainBox.addstr(1, 1, "Radio: {}".format(radio.currentlyPlaying))
		mainBox.addstr(2, 1, "Chanson: {}".format(radio.song))
		i = 4
		for r, url in radio.radios.items():
			if radio.selected == i - 3:
				mainBox.addstr(i, 4, "{}".format(r), curses.color_pair(1))
			else:
				mainBox.addstr(i, 4, "{}".format(r))
			mainBox.addstr(i, 1, "{}".format("->"))
			i+=1

	elif config["mode"] == 2:
		mainBox.clear()
		i = 1
		for m in chat.messages:
			if len(m.split(" - ")) > 1:
				splited = m.split(" - ")
				sender = splited[0]
				msg = splited[1]
				# if sender == chat.nickname:
				# 	mainBox.addstr(i, 1, str(sender), curses.color_pair(2))
				# else:
				config["debug"] = sender
				if not sender in chat.connected:
					mainBox.addstr(i, 1, str(sender), curses.color_pair(7))
					mainBox.addstr(i, 2 + len(sender), str(msg))
					mainBox.addstr(i, 3 + len(sender) + len(str(msg)), "(hors ligne)", curses.color_pair(7))
				else:
					mainBox.addstr(i, 1, str(sender), curses.color_pair((chat.connected.index(sender) + 4)))
					mainBox.addstr(i, 2 + len(sender), str(msg))
				if len(m) > curses.COLS:
					i += 2
				else:
					i+=1

	elif config["mode"] == 3:
		mainBox.clear()
		i = 2
		x = 0
		total = tracker.getActivity()
		if len(tracker.getActivity()) > 0:
			headerOffset = 7 
			mainBox.addstr(i, headerOffset + 1, "<", curses.color_pair(1))
			mainBox.addstr(i, headerOffset + 3, "{}".format(total[tracker.selectedDay]["date"]))
			mainBox.addstr(i, headerOffset + 12, ">".format(total[tracker.selectedDay]["date"]), curses.color_pair(1))
			i+=2

			mainBox.addstr(i, 2, "Projet", curses.color_pair(1))
			mainBox.addstr(i, 40, "Durée", curses.color_pair(1))
			i+=2
			if len(total[tracker.selectedDay]["activity"]) == 1:
				for k, a in total[tracker.selectedDay]["activity"].items():
					mainBox.addstr(i + 1, 2 , "En cours depuis {} :".format(tracker.last), curses.color_pair(6))
					mainBox.addstr(i + 1, 23 + len(tracker.last), "{}".format(tracker.current))
		
			else:
				for k, a in total[tracker.selectedDay]["activity"].items():
					if x > 0:
						duree = datetime.strptime(k, '%H:%M:%S') - datetime.strptime(previousKey, '%H:%M:%S')
						mainBox.addstr(i, 2, previousValue)
						mainBox.addstr(i, 40,"{}".format(duree))
					previousKey = k
					previousValue = a
					i+=1
					x+=1
				mainBox.addstr(i + 1, 2 , "En cours depuis {} :".format(tracker.last), curses.color_pair(6))
				mainBox.addstr(i + 1, 21 + len(tracker.last), "{}".format(tracker.current))
		else:
			mainBox.addstr(i, 2, "Aucune activité, démarrer avec /workon <projet>")

	elif config["mode"] == 4:
		mainBox.clear()
		mainBox.addstr(2, 2, "Todo")
		mainBox.addstr(2, 50, "Status")
		i = 4
		if len(list(todo.todos.keys())) > 0:
			for index, task in todo.todos.items():
				if index == todo.selected:
					mainBox.addstr(i, 2, f'{index} => {task["task"]}', curses.color_pair(1))
				else:
					mainBox.addstr(i, 2, f'{index} => {task["task"]}')

				mainBox.addstr(i, 50, task["status"], curses.color_pair(task["color"]))
				i+=1
		else:
			mainBox.addstr(i, 2, "Aucun todo en cours", curses.color_pair(100))
			mainBox.addstr(i + 1, 2, "/todo <tache> pour commencer", curses.color_pair(100))

	elif config["mode"] == 5:
			t = config["mt"]
			if not t.is_alive() and config["neo"] == True:
				config["mt"] = threading.Thread(target=rain, args=(mainBox, config))
				config["mt"].start()
			elif config["neo"] == False:
				mainBox.clear()
				mainBox.addstr(int(curses.LINES / 2) - 10, int(curses.COLS / 2) - 10, "YOU LEFT THE MATRIX", curses.color_pair(46))
				mainBox.addstr(int(curses.LINES / 2) - 9, int(curses.COLS / 2) - 10, "THERE IS NO GOING BACK", curses.color_pair(46))
				mainBox.refresh

	elif config["mode"] == 6:
		numbers = [
			[
				[" ", "_", "_", "__  "],
				[" ", "|", " ", "  | "],
				[" ", "|", " ", "  | "],
				[" ", "|", " ", "  | "],
				[" ", "|", " ", "  | "],
				[" ", "|_", "_", "__| "],
				[" ", " ", " ", "    "],
			],
			[
				[" ", " ", " ", "    "],
				[" ", " ", " ", "/|  "],
				[" ", " ", "/", " |  "],
				[" ", "/", " ", " |  "],
				[" ", " ", " ", " |  "],
				[" ", " ", " ", " |  "],
				[" ", " ", " ", "    "],
			],
			[
				[" ", "_", "_", "__  "],
				[" ", " ", " ", "  | "],
				[" ", " _", "_", "__| "],
				[" ", "|", " ", "    "],
				[" ", "|", " ", "    "],
				[" ", "|__", "_", "__  "],
				[" ", " ", " ", "    "],
			],
			[
				[" ", "_", "_", "__  "],
				[" ", " ", " ", "  | "],
				[" ", "_", "_", "__| "],
				[" ", " ", " ", "  | "],
				[" ", " ", " ", "  | "],
				[" ", "_", "_", "__| "],
				[" ", " ", " ", "    "],
			],
			[
				[" ", " ", " ", "    "],
				[" ", "|", " ", "  | "],
				[" ", "|_", "_", "__| "],
				[" ", " ", " ", "  | "],
				[" ", " ", " ", "  | "],
				[" ", " ", " ", "  | "],
				[" ", " ", " ", "    "],
			],
			[
				[" ", "_", "_", "___ "],
				[" ", "| ", "  ", "    "],
				[" ", "|_", "_", "__  "],
				[" ", " ", " ", "  | "],
				[" ", " ", " ", "  | "],
				[" ", "_", "_", "__| "],
				[" ", " ", " ", "    "],
			],
			[
				[" ", "_", "_", "__  "],
				[" ", "|", "  ", "    "],
				[" ", "|_", "_", "__  "],
				[" ", "|", " ", "  | "],
				[" ", "|", " ", "  | "],
				[" ", "|_", "_", "__| "],
				[" ", " ", " ", "    "],
			],
			[
				[" ", "_", "_", "__  "],
				[" ", " ", " ", " |  "],
				[" ", " ", " ", " |  "],
				[" ", " ", " ", " |  "],
				[" ", " ", " ", " |  "],
				[" ", " ", " ", " |  "],
				[" ", " ", " ", "    "],
			],
			[
				[" ", "_", "_", "__  "],
				[" ", "|", " ", "  | "],
				[" ", "|_", "_", "__| "],
				[" ", "|", " ", "  | "],
				[" ", "|", " ", "  | "],
				[" ", "|_", "_", "__| "],
				[" ", " ", " ", "    "],
			],
			[
				[" ", "_", "_", "__  "],
				[" ", "|", " ", "  | "],
				[" ", "|_", "_", "__| "],
				[" ", " ", " ", "  | "],
				[" ", " ", " ", "  | "],
				[" ", "_", "_", "__| "],
				[" ", " ", " ", "    "],
			],
			
		]

		points = [
			"",
			"",
			" ",
			"",
			" ",
			"",
			"",
		]
		mainBox.clear()
		if pomodoro.isPause == True:
			mainBox.addstr(2, 2, "Break Time - mode {}".format("automatique" if pomodoro.auto else "manuel"))
		else:
			mainBox.addstr(2, 2, "Pomodoro Time - mode {}".format("automatique" if pomodoro.auto else "manuel"))

		minutes = list(str(math.floor(pomodoro.duration / 60)))
		if len(minutes) == 1:
			minutes.insert(0, "0")
		seconds = list(str(pomodoro.duration % 60))
		if len(seconds) == 1:
			seconds.insert(0, "0")
		x = 0
		for number in minutes:
			y = 4
			currentNumber = numbers[int(number)]
			for line in currentNumber:
				for index, char in enumerate(line):
					if pomodoro.duration == 0:
						mainBox.addstr(y, x + index + 3, char, curses.color_pair(11))
					else:
						if pomodoro.isPaused == True:
							mainBox.addstr(y, x + index + 3, char, curses.color_pair(13))
						elif pomodoro.isPause == True:
							mainBox.addstr(y, x + index + 3, char, curses.color_pair(12))
						else:
							mainBox.addstr(y, x + index + 3, char, curses.color_pair(10))
				y+=1
			x+=8

		y = 2
		x+=3
		for i, ch in enumerate(points):
			mainBox.addstr(y + i, x, ch, curses.color_pair(10))
			y+=1

		for second in seconds:
			y = 4
			currentNumber = numbers[int(second)]
			for line in currentNumber:
				for index, char in enumerate(line):
					if pomodoro.duration == 0:
						mainBox.addstr(y, x + index + 3, char, curses.color_pair(11))
					else:
						if pomodoro.isPaused == True:
							mainBox.addstr(y, x + index + 3, char, curses.color_pair(13))
						elif pomodoro.isPause == True:
							mainBox.addstr(y, x + index + 3, char, curses.color_pair(12))
						else:
							mainBox.addstr(y, x + index + 3, char, curses.color_pair(10))
				y+=1
			x+=8

		y += 2
		x = 2
		
		for i, command in enumerate(pomodoro.commands):
			if pomodoro.selected == i:
				mainBox.addstr(y, x, command, curses.color_pair(1))
			else:
				mainBox.addstr(y, x, command)
			x += len(command)
			x += 4

		# mainBox.addstr(4, 4, minutes[0])
		# mainBox.addstr(4, 7, seconds[0])
		mainBox.refresh()



def help(config, mainBox, manpage):
	mainBox.clear()
	mainBox.addstr(1, 3, "Action\t\t\t\tCommande")
	for i, line in enumerate(manpage.lines):
		if manpage.selected == i:
			mainBox.addstr(line["y"], 1, "->", curses.color_pair(1))
		mainBox.addstr(line["y"], line["x"], line["str"], curses.color_pair(line["color"]))