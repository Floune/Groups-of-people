import curses
import json

class Todo:
	def __init__(self):
		self.todos = {}
		self.datafile = "todo.json"
		self.selected = "0"
		self.maybeTodo()

	def maybeTodo(self):
		with open(self.datafile, "r") as json_file:
			todos = json.load(json_file)
			for i, task in todos.items():
				tmp = {
					i: {
						"task": task["task"],
						"status": task["status"],
						"color": task["color"],
					}
				}
				self.todos.update(tmp)
			


	def updateSelection(self, key: str):
		if key == "KEY_DOWN" or key == "KEY_RIGHT":
			up = int(self.selected)
			up += 1
			if up > len(list(self.todos.keys())) -1:
				up = 0

		if key == "KEY_UP" or key == "KEY_LEFT":
			up = int(self.selected)
			up -= 1
			if up == -1:
				up = len(list(self.todos.keys())) -1
		self.selected = str(up)



	def addTodo(self, task: str):
		self.todos.update({
			str(len(list(self.todos.keys()))): {
				"task": task,
				"status": "En cours",
				"color": 1
			}
		})
		with open(self.datafile, "w") as json_file:				
				json.dump(self.todos, json_file)

	def toggle(self):
		if len(list(self.todos.keys())) > 0:
			if self.todos[self.selected]["status"] == "En cours":
				update = {
					self.selected: {
						"task": self.todos[self.selected]["task"],
						"status": "Terminé",
						"color": 4
					}
				}
			else:
				update = {
					self.selected: {
						"task": self.todos[self.selected]["task"],
						"status": "En cours",
						"color": 1
					}
				}
			self.todos.update(update)

	def done(self):
		self.todos.pop(self.selected, None)
		newTodo = {}
		x = 0
		for index, task in self.todos.items():
			update = {
				str(x): {
					"task": task["task"],
					"status": task["status"],
					"color": task["color"]
				}
			}
			newTodo.update(update)
			x+=1
		self.todos = newTodo
		with open(self.datafile, "w") as json_file:				
			json.dump(self.todos, json_file)

			



def todof(config, command, radio, chat, tracker, todo):	
	config["mode"] = 4

	if command in config["arrows"]:
		config["debug"] = "megaradio" + command
		todo.updateSelection(command)

	elif "/todo " in command:
		todo.addTodo(command[6:])

	elif command == "":
		config["debug"] = "grougnu"
		todo.toggle()

	elif command == "KEY_DC":
		config["debug"] = "Todo deleted"
		todo.done()