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


def chatf(config, command, radio, chat, tracker, todo, manpage, pomodoro):
	config["mode"] = 2
	if command in config["arrows"]:
		chat.select(command)
	elif command == "/annoy":
		config["annoy"] = not config["annoy"]
	elif command and command not in config["arrows"]:
		chat.sendMessage(command)

def receiveChat(connection, gui_q, chat, config):
	while True:
		try:
			msg = connection.recv(1024)
			if msg:
				decoded = msg.decode()
				if "###nickname###" in decoded:
					splited = decoded.split(" - ")
					chat.nickname = splited[1]
				elif "###connected###" in decoded:
					splited = decoded.split(" - ")
					chat.connected = splited[1].split(", ")
				else:
					chat.addMessage(decoded)
				gui_q.put("q")
				maybePlaySound(decoded, config, chat.nickname)
			else:
				connection.close()
				break

		except Exception as e:
			connection.close()
			break


def maybePlaySound(decoded, config, nickname):
	splited = decoded.split(" - ")
	sender = splited[0]
	if nickname != sender and not "###" in sender and config["annoy"] == True and config["mode"] != 2:
		player = vlc.MediaPlayer("message.mp3")
		player.play()
		time.sleep(3)
		player.release()
	else:
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