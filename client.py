import socket, threading, queue
import curses
import sys
from input import * 
from gui import *
from radio import Radio

input_queue = queue.Queue()
gui_queue = queue.Queue()

def pagedead(config, command):
	mode = 0
	config["debug"] = "pagedead requested"

def radiof(config, command):
	mode = 1
	config["debug"] = "radio requested"


def main(stdscr):
	config = {
		'debug': "debug zone",
		'commands' : ['help', 'radio'],
		'modes': {
			0 : {
				"title": "Page Dead",
				"func": pagedead
			},
			1 : {
				"title": "Radio",
				"func": radiof
			}
		},
		'mode': 0

	}

	txtBox = curses.newwin(4, curses.COLS, curses.LINES - 5, 0)
	toolBox = curses.newwin(7, curses.COLS, 0, 0)
	mainBox = curses.newwin(curses.LINES - 12, curses.COLS, 7, 0)
	initTeams(stdscr, toolBox, mainBox, txtBox)

	radio = Radio()

	writeThread = threading.Thread(target=waitInput, args=(input_queue, txtBox))
	writeThread.start()
	logicThread = threading.Thread(target=logicLoop, args=(config, input_queue, gui_queue))
	logicThread.start()
	guiThread = threading.Thread(target=gui, args=(config, gui_queue, txtBox, toolBox, mainBox))
	guiThread.start()


	writeThread.join()
	mainThread.join()
	guiThread.join()


def logicLoop(config, input_q, gui_q):

	command = ""
	while command != "/quit":
		command = input_q.get()

		if command[0] == "/":
			handleCommand(config, command[1:])

		gui_q.put(command)

	endTeams()

def handleCommand(config, command):
	if command in config["commands"]:
		config["mode"] = config["commands"].index(command)
		config["modes"][config["mode"]]["func"](config, command)

def initTeams(stdscr, toolBox, mainBox, txtBox):
	curses.noecho()
	curses.cbreak()
	stdscr.clear()
	curses.curs_set(False)
	toolBox.box()
	mainBox.box()
	txtBox.box()
	toolBox.refresh()
	txtBox.refresh()
	mainBox.refresh()
	if curses.has_colors():
		curses.start_color()
		curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
		curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)

def endTeams():
	curses.nocbreak()
	curses.curs_set(True)
	curses.endwin()
	sys.exit(1)


curses.wrapper(main)