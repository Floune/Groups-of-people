import socket, threading, queue
from input import * 
import curses
import sys

input_queue = queue.Queue()
gui_queue = queue.Queue()

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
	toolBox = curses.newwin(7, curses.COLS, 0, 0)
	mainBox = curses.newwin(curses.LINES - 12, curses.COLS, 7, 0)
	txtBox.keypad(True)
	txtBox.clear()
	txtBox.box()
	txtBox.refresh()
	writeThread = threading.Thread(target=waitInput, args=(input_queue, txtBox))
	writeThread.start()
	mainThread = threading.Thread(target=mainLoop, args=(input_queue, gui_queue))
	mainThread.start()
	guiThread = threading.Thread(target=gui, args=(gui_queue, txtBox, toolBox, mainBox))
	guiThread.start()


	writeThread.join()
	mainThread.join()
	guiThread.join()


def mainLoop(input_q, gui_q):

	command = ""
	while command != "/quit":
		command = input_q.get()
		gui_q.put(command)
	endTeams()
	

def gui(gui_q, txtBox, toolBox, mainBox):
	toolBox.box()
	mainBox.box()
	toolBox.refresh()
	mainBox.refresh()
	command = ""
	i=1

	while command != "/quit":
		command = gui_q.get()
		if command:
			mainBox.addstr(i, 2, str(command))
			i+=1
		txtBox.clear()
		txtBox.box()
		txtBox.refresh()
		mainBox.box()
		mainBox.refresh()

def endTeams():
	curses.nocbreak()
	curses.curs_set(True)
	curses.endwin()
	sys.exit(1)


curses.wrapper(main)