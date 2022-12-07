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


