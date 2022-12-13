import curses

def initTeams(stdscr, toolBox, mainBox, txtBox):
	curses.noecho()
	curses.cbreak()
	stdscr.clear()
	curses.curs_set(False)
	txtBox.keypad(True)
	toolBox.box()
	mainBox.box()
	txtBox.box()
	toolBox.refresh()
	txtBox.refresh()
	mainBox.refresh()
	if curses.has_colors():
		curses.start_color()
		curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
		curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)
		curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)
		curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLUE)
		curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
		curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_CYAN)
		curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_RED)

def endTeams():
	curses.nocbreak()
	curses.curs_set(True)
	curses.endwin()
	sys.exit(1)
