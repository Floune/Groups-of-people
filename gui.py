import curses
from datetime import date, datetime


def gui(config, gui_q, txtBox, toolBox, mainBox, radio, chat, tracker, todo):
	command = ""
	i=1

	while command != "/quit":
		tools(toolBox, config, chat)
		command = gui_q.get()
		main(mainBox, config, radio, chat, tracker, todo)
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
	if config["mode"] == 2:
		toolBox.addstr(3, 2, "<", curses.color_pair(1)) 
		if chat.selectedConnectedUser == -1:
			toolBox.addstr(3, 4, "{} {}".format(len(chat.connected), "utilisateurs connectés" if len(chat.connected) > 1 else "utilisateur connecté"))
			toolBox.addstr(3, 29, ">", curses.color_pair(1)) 
		elif chat.selectedConnectedUser >= 0 and chat.selectedConnectedUser < len(chat.connected):
			toolBox.addstr(3, 4, "{}".format(chat.connected[chat.selectedConnectedUser]), curses.color_pair((chat.connected.index(chat.connected[chat.selectedConnectedUser]) + 1)))
			toolBox.addstr(3, 5 + len(chat.connected[chat.selectedConnectedUser]), ">", curses.color_pair(1)) 

	toolBox.box()
	toolBox.refresh()

def main(mainBox, config, radio, chat, tracker, todo):
	if config["mode"] == 0:
		help(config, mainBox)
		
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
					mainBox.addstr(i, 1, str(sender), curses.color_pair((chat.connected.index(sender) + 1)))
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
			mainBox.addstr(i, 20, "Durée", curses.color_pair(1))
			i+=2
			if len(total[tracker.selectedDay]["activity"]) == 1:
				for k, a in total[tracker.selectedDay]["activity"].items():
					mainBox.addstr(i, 2, "Début de journée à {} sur {}".format(k, a))
			else:
				for k, a in total[tracker.selectedDay]["activity"].items():
					if x > 0:
						duree = datetime.strptime(k, '%H:%M:%S') - datetime.strptime(previousKey, '%H:%M:%S')
						mainBox.addstr(i, 2, previousValue)
						mainBox.addstr(i, 21,"{}".format(duree))
					previousKey = k
					previousValue = a
					i+=1
					x+=1
				mainBox.addstr(i + 1, 2 , "En cours depuis {} :".format(tracker.last), curses.color_pair(6))
				mainBox.addstr(i + 1, 23 + len(tracker.last), "{}".format(tracker.current))
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
			mainBox.addstr(i, 2, "Aucun todo en cours", curses.color_pair(1))
			mainBox.addstr(i + 1, 2, "/todo <tache> pour commencer", curses.color_pair(1))


def help(config, mainBox):
	mainBox.clear()

	wtf = {
		0: {
			"x": 2,
			"y": 3,
			"str": "Radio",
			"color": curses.color_pair(0),
		},
		1: {
			"x": 40,
			"y": 3,
			"str": "/radio",
			"color": curses.color_pair(0),
		},
		2: {
			"x": 2,
			"y": 4,
			"str": "Chat",
			"color": curses.color_pair(0),
		},
		3: {
			"x": 40,
			"y": 4,
			"str": "/chat",
			"color": curses.color_pair(0),
		},
		4: {
			"x": 2,
			"y": 5,
			"str": "Aide",
			"color": curses.color_pair(0),
		},
		5: {
			"x": 40,
			"y": 5,
			"str": "/help",
			"color": curses.color_pair(0),
		},
		6: {
			"x": 2,
			"y": 6,
			"str": "Todo list",
			"color": curses.color_pair(0),
		},
		7: {
			"x": 40,
			"y": 6,
			"str": "/todo",
			"color": curses.color_pair(0),
		},
		8: {
			"x": 2,
			"y": 8,
			"str": "Démarrer le tracker",
			"color": curses.color_pair(0),
		},
		9: {
			"x": 40,
			"y": 8,
			"str": "/workon <project>",
			"color": curses.color_pair(0),
		},
		10: {
			"x": 2,
			"y": 7,
			"str": "Activity Tracker",
			"color": curses.color_pair(0),
		},
		11: {
			"x": 40,
			"y": 7,
			"str": "/tracker",
			"color": curses.color_pair(0),
		},
		12: {
			"x": 2,
			"y": 9,
			"str": "Undo",
			"color": curses.color_pair(0),
		},
		13: {
			"x": 40,
			"y": 9,
			"str": "/undo",
			"color": curses.color_pair(0),
		},
		14: {
			"x": 2,
			"y": 10,
			"str": "Nouveau todo",
			"color": curses.color_pair(0),
		},
		15: {
			"x": 40,
			"y": 10,
			"str": "/todo <tache>",
			"color": curses.color_pair(0),
		},
		16: {
			"x": 2,
			"y": 11,
			"str": "Quitter",
			"color": curses.color_pair(0),
		},
		17: {
			"x": 40,
			"y": 11,
			"str": "/quit",
			"color": curses.color_pair(0),
		},
		18: {
			"x": 2,
			"y": 1,
			"str": "Action",
			"color": curses.color_pair(0),
		},
		19: {
			"x": 40,
			"y": 1,
			"str": "Commande",
			"color": curses.color_pair(0),
		},

	}
	for key, line in wtf.items():
		mainBox.addstr(line["y"], line["x"], line["str"], line["color"])