import socket, threading, queue
from input import * 
import curses
import sys

q = queue.Queue()

def main(stdscr):
	# Clear screen
	curses.noecho()
	curses.cbreak()
	stdscr.clear()
	curses.curs_set(False)
	if curses.has_colors():
		curses.start_color()
		curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
		curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
	txtBox = curses.newwin(4, curses.COLS, curses.LINES - 5, 0)
	txtBox.keypad(True)
	txtBox.clear()
	txtBox.box()
	txtBox.refresh()
	writeThread = threading.Thread(target=waitInput, args=(q, txtBox))
	writeThread.start()
	mainThread = threading.Thread(target=mainLoop, args=(q, txtBox))
	mainThread.start()
	writeThread.join()
	mainThread.join()


def mainLoop(queue, txtBox):
	toolBox = curses.newwin(7, curses.COLS, 0, 0)
	mainBox = curses.newwin(curses.LINES - 12, curses.COLS, 7, 0)
	toolBox.box()
	mainBox.box()
	toolBox.refresh()
	mainBox.refresh()
	output = ""
	i=1
	while output != "/quit":
		output = queue.get()
		msg = "".join(output)
		if msg:
			mainBox.addstr(i, 2, str(msg))
			i+=1
		txtBox.clear()
		txtBox.box()
		txtBox.refresh()
		mainBox.box()
		mainBox.refresh()
	endTeams()
	

def endTeams():
	curses.nocbreak()
	curses.curs_set(True)
	curses.endwin()
	sys.exit(1)


curses.wrapper(main)