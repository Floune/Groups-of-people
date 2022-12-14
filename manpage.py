import random
import curses

def pagedead(config, command, radio, chat, tracker, todo):
	config["mode"] = 0
	config["debug"] = command

	if command in config["arrows"]:
		config["manpage"]["command_color"] = random.randint(2, curses.COLORS)
		config["manpage"]["action_color"] = random.randint(2, curses.COLORS)
