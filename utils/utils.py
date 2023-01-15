import curses

def initTeams(stdscr, toolBox, mainBox, txtBox):
	if curses.has_colors():
		curses.use_default_colors()
		for i in range(0, curses.COLORS):
		    curses.init_pair(i, i, -1);
		curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
		curses.init_pair(10, curses.COLOR_BLACK, curses.COLOR_GREEN)
		curses.init_pair(11, curses.COLOR_BLACK, curses.COLOR_RED)
		curses.init_pair(12, curses.COLOR_BLACK, curses.COLOR_YELLOW)
		curses.init_pair(13, curses.COLOR_BLACK, curses.COLOR_BLUE)

	curses.noecho()
	curses.cbreak()
	curses.start_color()
	stdscr.clear()
	curses.curs_set(False)
	txtBox.keypad(True)
	toolBox.box()
	mainBox.box()
	txtBox.box()
	toolBox.refresh()
	txtBox.refresh()
	mainBox.refresh()
	


def endTeams():
	curses.nocbreak()
	curses.curs_set(True)
	curses.endwin()
	sys.exit(1)
