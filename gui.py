import curses

def gui(config, gui_q, txtBox, toolBox, mainBox, radio, chat):
	command = ""
	i=1

	while command != "/quit":
		tools(toolBox, config, chat)
		main(mainBox, config, radio, chat)
		command = gui_q.get()
		# if command:
		# 	mainBox.addstr(i, 2, str(command))
		# 	i+=1
		txtBox.clear()
		txtBox.box()
		txtBox.refresh()


def tools(toolBox, config, chat):
	toolBox.clear()
	toolBox.addstr(2, int(curses.COLS / 2 - 3), config["modes"][config["mode"]]["title"])
	toolBox.addstr(2, 2, str(config["mode"]))
	toolBox.box()
	toolBox.refresh()

def main(mainBox, config, radio, chat):
	if config["mode"] == 0:
		mainBox.clear()
		mainBox.addstr(2, 2, "Guide")
		mainBox.addstr(3, 2, "=====")
		mainBox.addstr(5, 2, "Radio : /radio")
		mainBox.addstr(6, 2, "Chat : /chat")
		mainBox.addstr(7, 2, "Aide : /help")
		mainBox.addstr(8, 2, "Quitter : /quit")

	elif config["mode"] == 1:
		mainBox.clear()
		mainBox.addstr(1, 1, "Radio: {}".format(radio.currentlyPlaying))
		mainBox.addstr(2, 1, "Song: {}".format(radio.song))
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
			mainBox.addstr(i, 1, str(m))
			if len(m) > curses.COLS:
				i += 2
			else:
				i+=1
		mainBox.box()

	mainBox.box()
	mainBox.refresh()