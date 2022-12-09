import socket, threading, queue
import curses
import sys
import os
from input import * 
from gui import *
from radio import *
from chat import *
from manpage import *
from activity import *


def main(stdscr):
	#Queues
	input_queue = queue.Queue()
	gui_queue = queue.Queue()

	#socket
	connection = socket.socket()
	connection.connect((os.environ.get('FLOUNE_CHAT_SERVER', 'localhost'), int(os.environ.get('FLOUNE_CHAT_PORT', 13000))))
	
	#shared objects
	config = {
		'arrows' : ["KEY_UP","KEY_DOWN","KEY_LEFT","KEY_RIGHT", "KEY_BACKSPACE"],
		'debug': "debug zone",
		'commands' : ['help', 'radio', 'chat', 'tracker'],
		'modes': {
			0 : {
				"title": "Page Dead",
				"func": pagedead
			},
			1 : {
				"title": "Radio",
				"func": radiof
			},
			2: {
				"title": "Chat",
				"func": chatf
			},
			3: {
				"title": "Activity Tracker",
				"func": trackf
			}
		},
		'mode': 0

	}
	radio = Radio()
	chat = Chat(curses.LINES - 17, connection, gui_queue)
	tracker = Tracker()


	#init windows
	txtBox = curses.newwin(4, curses.COLS, curses.LINES - 5, 0)
	toolBox = curses.newwin(7, curses.COLS, 0, 0)
	mainBox = curses.newwin(curses.LINES - 12, curses.COLS, 7, 0)
	initTeams(stdscr, toolBox, mainBox, txtBox)


	#Tous les threads de ta vie
	writeThread = threading.Thread(target=waitInput, args=(input_queue, txtBox))
	writeThread.start()
	logicThread = threading.Thread(target=logicLoop, args=(config, input_queue, gui_queue, radio, chat, tracker))
	logicThread.start()
	guiThread = threading.Thread(target=gui, args=(config, gui_queue, txtBox, toolBox, mainBox, radio, chat, tracker))
	guiThread.start()
	receiveThread = threading.Thread(target=receiveChat, args=(connection, gui_queue, chat))
	receiveThread.start()
	writeThread.join()
	receiveThread.join()
	logicThread.join()
	guiThread.join()


def logicLoop(config, input_q, gui_q, radio, chat, tracker):
	command = ""
	while command != "/quit":
		command = input_q.get()

		handleCommand(config, command, radio, chat, tracker)

		gui_q.put(command)

	chat.sendMessage("/quit")
	endTeams()

def handleCommand(config, command, radio, chat, tracker):
	if len(command) > 0 and command[0] == "/" and command[1:] in config["commands"]:
		config["mode"] = config["commands"].index(command[1:])
		config["modes"][config["mode"]]["func"](config, command, radio, chat, tracker)
	else:
		config["modes"][config["mode"]]["func"](config, command, radio, chat, tracker)

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
		curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
		curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)

def endTeams():
	curses.nocbreak()
	curses.curs_set(True)
	curses.endwin()
	sys.exit(1)


curses.wrapper(main)