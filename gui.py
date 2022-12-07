import curses

def gui(config, gui_q, txtBox, toolBox, mainBox):
	command = ""
	i=1

	while command != "/quit":
		tools(toolBox, config)
		command = gui_q.get()
		if command:
			mainBox.addstr(i, 2, str(command))
			i+=1
		txtBox.clear()
		txtBox.box()
		txtBox.refresh()
		mainBox.box()
		mainBox.refresh()

def tools(toolBox, config):
	toolBox.addstr(2, int(curses.COLS / 2 - 3), config["modes"][config["mode"]])
	toolBox.addstr(2, 2, config["debug"])
	toolBox.refresh()