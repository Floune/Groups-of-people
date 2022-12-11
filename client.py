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
from utils import *
from todo import *


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
		'commands' : ['help', 'radio', 'chat', 'tracker', 'todo'],
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
			},
			4: {
				"title": "Todo list",
				"func": todof
			}
		},
		'mode': 0

	}
	radio = Radio()
	chat = Chat(curses.LINES - 17, connection, gui_queue)
	tracker = Tracker()
	todo  = Todo()


	#init windows
	txtBox = curses.newwin(4, curses.COLS, curses.LINES - 5, 0)
	toolBox = curses.newwin(7, curses.COLS, 0, 0)
	mainBox = curses.newwin(curses.LINES - 12, curses.COLS, 7, 0)
	initTeams(stdscr, toolBox, mainBox, txtBox)


	#Tous les threads de ta vie
	writeThread = threading.Thread(target=waitInput, args=(input_queue, txtBox))
	writeThread.start()
	logicThread = threading.Thread(target=logicLoop, args=(config, input_queue, gui_queue, radio, chat, tracker, todo))
	logicThread.start()
	guiThread = threading.Thread(target=gui, args=(config, gui_queue, txtBox, toolBox, mainBox, radio, chat, tracker, todo))
	guiThread.start()
	receiveThread = threading.Thread(target=receiveChat, args=(connection, gui_queue, chat))
	receiveThread.start()
	writeThread.join()
	receiveThread.join()
	logicThread.join()
	guiThread.join()


def logicLoop(config, input_q, gui_q, radio, chat, tracker, todo):
	command = ""
	while command != "/quit":
		command = input_q.get()

		handleCommand(config, command, radio, chat, tracker, todo)

		gui_q.put(command)

	chat.sendMessage("/quit")
	endTeams()


def handleCommand(config, command, radio, chat, tracker, todo):
	if len(command) > 0 and command[0] == "/" and command[1:] in config["commands"]:
		config["mode"] = config["commands"].index(command[1:])
		config["modes"][config["mode"]]["func"](config, command, radio, chat, tracker, todo)
	else:
		config["modes"][config["mode"]]["func"](config, command, radio, chat, tracker, todo)



curses.wrapper(main)