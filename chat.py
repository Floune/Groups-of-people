import curses
import socket, threading

class Chat:

	def __init__(self, maxMessages, connection, gui_q):
		self.maxMessages = maxMessages
		self.gui_q = gui_q
		self.connection = connection
		self.messages = []

	def sendMessage(self, msg):
		if msg and isinstance(msg, str):
	 		self.connection.send(msg.encode())

	def addMessage(self, message):
		if len(message) > 0:
			self.messages.append(message)
			if len(self.messages) > self.maxMessages:
				self.messages.pop(0)




def chatf(config, command, radio, chat, tracker):
	config["mode"] = 2
	if command and command not in config["arrows"]:
		chat.sendMessage(command)

def receiveChat(connection, gui_q, chat):
	while True:
		try:
			msg = connection.recv(1024)
			if msg:
				decoded = msg.decode()
				if "###nickname###" in decoded:
					splited = decoded.split(" - ")
					chat.nickname = splited[1]
				else:
					chat.addMessage(decoded)
				gui_q.put("q")
			else:
				connection.close()
				break

		except Exception as e:
			connection.close()
			break

