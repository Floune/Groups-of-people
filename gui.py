import curses
from datetime import date, datetime


def gui(config, gui_q, txtBox, toolBox, mainBox, radio, chat, tracker):
	command = ""
	i=1

	while command != "/quit":
		tools(toolBox, config, chat)
		command = gui_q.get()
		main(mainBox, config, radio, chat, tracker)
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
	toolBox.addstr(2, 2, str(config["mode"]))
	toolBox.box()
	toolBox.refresh()

def main(mainBox, config, radio, chat, tracker):
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
				mainBox.addstr(i, 4, "{}".format(r), curses.color_pair(2))
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
				if sender == chat.nickname:
					mainBox.addstr(i, 1, str(sender), curses.color_pair(2))
				else:
					mainBox.addstr(i, 1, str(sender), curses.color_pair(1))
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
			mainBox.addstr(i, headerOffset + 1, "<", curses.color_pair(2))
			mainBox.addstr(i, headerOffset + 3, "{}".format(total[tracker.selectedDay]["date"]))
			mainBox.addstr(i, headerOffset + 12, ">".format(total[tracker.selectedDay]["date"]), curses.color_pair(2))
			i+=2

			mainBox.addstr(i, 2, "Projet", curses.color_pair(2))
			mainBox.addstr(i, 20, "Durée", curses.color_pair(2))
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
				mainBox.addstr(i + 1, 2 , "En cours: {} - depuis {}".format(tracker.current, tracker.last))
		else:
			mainBox.addstr(i, 2, "Aucune activité, démarrer avec /workon <projet>")

def help(config, mainBox):
	mainBox.clear()

	wtf = {
		0: {
			"x": 2,
			"y": 2,
			"str": "Radio: /radio",
			"color": curses.color_pair(3),
		},
		1: {
			"x": 2,
			"y": 3,
			"str": "Chat: /chat",
			"color": curses.color_pair(3),
		},
		2: {
			"x": 2,
			"y": 4,
			"str": "Aide: /help",
			"color": curses.color_pair(3),
		},
		3: {
			"x": 2,
			"y": 6,
			"str": "Démarrer le tracker: /workon <project>",
			"color": curses.color_pair(3),
		},
		5: {
			"x": 2,
			"y": 7,
			"str": "Undo: /undo",
			"color": curses.color_pair(3),
		},
		6: {
			"x": 2,
			"y": 8,
			"str": "Quitter: /quit",
			"color": curses.color_pair(3),
		},
		7: {
			"x": 2,
			"y": 1,
			"str": "Commandes",
			"color": curses.color_pair(2),
		},
		8: {
			"x": 2,
			"y": 5,
			"str": "Activity Tracker: /tracker",
			"color": curses.color_pair(3),
		},

	}
	for key, line in wtf.items():
		mainBox.addstr(line["y"], line["x"], line["str"], line["color"])