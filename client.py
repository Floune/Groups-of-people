import socket, threading, queue
import curses
import sys
from input import * 
from gui import *
from radio import Radio
from chat import Chat

input_queue = queue.Queue()
gui_queue = queue.Queue()

def pagedead(config, command, radio, chat):
	config["mode"] = 0
	config["debug"] = command

def radiof(config, command, radio, chat):	
	config["mode"] = 1

	if command in config["arrows"]:
		config["debug"] = "megaradio" + command
		radio.updateSelection(command)

	elif command == "":
		radio.select()

def chatf(config, command, radio, chat):
	config["mode"] = 2
	if command:
		chat.sendMessage(command)

def main(stdscr):
	SERVER_ADDRESS = '127.0.0.1'
	SERVER_PORT = 13000
	connection = socket.socket()
	connection.connect((SERVER_ADDRESS, SERVER_PORT))
	config = {
		'arrows' : ["KEY_UP","KEY_DOWN","KEY_LEFT","KEY_RIGHT"],
		'debug': "debug zone",
		'commands' : ['help', 'radio', 'chat'],
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
			}
		},
		'mode': 1

	}

	txtBox = curses.newwin(4, curses.COLS, curses.LINES - 5, 0)
	toolBox = curses.newwin(7, curses.COLS, 0, 0)
	mainBox = curses.newwin(curses.LINES - 12, curses.COLS, 7, 0)
	initTeams(stdscr, toolBox, mainBox, txtBox)

	radio = Radio()
	chat = Chat(curses.LINES - 17, connection, gui_queue)

	writeThread = threading.Thread(target=waitInput, args=(input_queue, txtBox))
	writeThread.start()
	logicThread = threading.Thread(target=logicLoop, args=(config, input_queue, gui_queue, radio, chat))
	logicThread.start()
	guiThread = threading.Thread(target=gui, args=(config, gui_queue, txtBox, toolBox, mainBox, radio, chat))
	guiThread.start()
	receiveThread = threading.Thread(target=receiveChat, args=(connection, gui_queue, chat))
	receiveThread.start()
	
	writeThread.join()
	receiveThread.join()
	logicThread.join()
	guiThread.join()



def receiveChat(connection, gui_q, chat):
	while True:
		try:
			msg = connection.recv(1024)
			if msg:
				decoded = msg.decode()
				if decoded[0] == "/":
					chat.addMessage("command received from server")
				else:
					chat.addMessage(decoded)
				gui_q.put("q")
			else:
				connection.close()
				break

		except Exception as e:
			connection.close()
			break



def logicLoop(config, input_q, gui_q, radio, chat):
	command = ""
	while command != "/quit":
		command = input_q.get()

		handleCommand(config, command, radio, chat)

		gui_q.put(command)

	chat.sendMessage("/quit")
	endTeams()

def handleCommand(config, command, radio, chat):
	if len(command) > 0 and command[0] == "/" and command[1:] in config["commands"]:
		config["mode"] = config["commands"].index(command[1:])
		config["modes"][config["mode"]]["func"](config, command, radio, chat)
	else:
		config["modes"][config["mode"]]["func"](config, command, radio, chat)

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