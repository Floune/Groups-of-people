import curses
from datetime import date, datetime


def gui(config, gui_q, txtBox, toolBox, mainBox, radio, chat, tracker):
	command = ""
	i=1

	while command != "/quit":
		tools(toolBox, config, chat)
		main(mainBox, config, radio, chat, tracker)
		command = gui_q.get()
		# if command:
		# 	mainBox.addstr(i, 2, str(command))
		# 	i+=1
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
		mainBox.clear()
		mainBox.addstr(2, 2, "Navigation", curses.color_pair(2))
		mainBox.addstr(4, 2, "Radio : /radio")
		mainBox.addstr(5, 2, "Chat : /chat")
		mainBox.addstr(6, 2, "Aide : /help")
		mainBox.addstr(7, 2, "Tracker : /tracker")

		mainBox.addstr(9, 2, "Activity tracker", curses.color_pair(2))
		mainBox.addstr(11, 2, "Tracker un projet : /workon <project>")
		mainBox.addstr(12, 2, "Changer de semaine : flèches gauche/droite")
		mainBox.addstr(13, 2, "Undo : /undo")

		mainBox.addstr(14, 2, "Quitter : /quit")

	elif config["mode"] == 1:
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
	mainBox.box()
	mainBox.refresh()