import curses
import socket, threading
import vlc
import time

class Chat:

	def __init__(self, maxMessages, connection, gui_q):
		self.maxMessages = maxMessages
		self.gui_q = gui_q
		self.connection = connection
		self.messages = []
		self.connected = []
		self.selectedConnectedUser = -1
		self.nickname = ""

	def sendMessage(self, msg):
		if msg and isinstance(msg, str):
	 		self.connection.send(msg.encode())

	def addMessage(self, message):
		if len(message) > 0:
			self.messages.append(message)
			if len(self.messages) > self.maxMessages:
				self.messages.pop(0)

	def select(self, key):
		if key == "KEY_DOWN" or key == "KEY_RIGHT":
			if self.selectedConnectedUser < len(self.connected) - 1:
				self.selectedConnectedUser += 1
		if key == "KEY_UP" or key == "KEY_LEFT":
			if self.selectedConnectedUser > -1:
				self.selectedConnectedUser -= 1


def chatf(config, command, radio, chat, tracker, todo):
	config["mode"] = 2
	if command in config["arrows"]:
		chat.select(command)
	elif command and command not in config["arrows"]:
		chat.sendMessage(command)

def receiveChat(connection, gui_q, chat):
	while True:
		try:
			msg = connection.recv(1024)
			if msg:
				decoded = msg.decode()
				maybePlaySound(decoded)
				if "###nickname###" in decoded:
					splited = decoded.split(" - ")
					chat.nickname = splited[1]
				elif "###connected###" in decoded:
					splited = decoded.split(" - ")
					chat.connected = splited[1].split(", ")
				else:
					chat.addMessage(decoded)
				gui_q.put("q")
			else:
				connection.close()
				break

		except Exception as e:
			connection.close()
			break


def maybePlaySound(decoded):
	keywords = ["lol", "^^", "haha", "prout", "bravo"]
	sounds = {
		"lol" : "laugh.mp3",
		"^^": "laugh.mp3",
		"haha": "laugh.mp3",
		"prout": "fart.mp3",
		"bravo": "applause.mp3"
	}
	splited = decoded.split(" - ")
	keyword = splited[1]
	if keyword in keywords:
		player = vlc.MediaPlayer(sounds[keyword])
		player.play()
		time.sleep(2)
		player.release()