import curses
import random
import time
import threading

def matrix(config, command, radio, chat, tracker, todo, manpage):
	config["mode"] = 5
	if "/reality" in command:
		config["mode"] = 0
		config["neo"] = False		
		config["mt"].join()
		config["modes"][5]["title"] = "You already know kung-fu"
		#config["mt"] = threading.Thread(target=rain, args=(mainBox, config))


	elif command in config["arrows"]:
		config["neolor"] = random.randint(0, curses.COLORS)
 
	
def rain(mainBox, config):
	config["neo"] == False
	greens = [46, 40, 34, 28, 22]
	chars = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
             "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
             "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
             "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
             "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "!", "#", "$",
             "%", "^", "&", "(", ")", "-", "+", "=", "[", "]", "{", "}", "|",
             ";", ":", "<", ">", ",", ".", "?", "~", "`", "@", "*", "_", "'",
             "\\", "/", '"']

	w = curses.COLS - 2
	h = curses.LINES - 13
	screen = [ [" "]*w for i in range(h)]
	bars = []
	bar = createBar(chars, greens)
	bars.append(bar)
	x = 0
	while config["neo"] == True:
		for e in range(2):
			bars.append(createBar(chars, greens))
		i = 0
		updateScreen(screen, bars)

		tick = parseScreen(screen)
		for line in tick:
			mainBox.addstr(i, 0, str(line), curses.color_pair(config["neolor"]))
			i+=1
		mainBox.refresh()
		time.sleep(0.2)
		x+=1
	config["mode"] = 0



def parseScreen(screen):
	tick = []
	for line in screen:
		tmp = ""
		for char in line:
			tmp += char
		tick.append(tmp)
	return tick

def createBar(chars, greens):
	bar = []
	for z in range(11):
		bar.append(chars[random.randint(0, len(chars) - 1)])
	return {"x": random.randint(0, curses.COLS - 2), "y": -6, "chars": bar}

def updateScreen(screen, bars):
	for b in bars:
		for i, c in enumerate(b["chars"]):
			if b["y"] + i < curses.LINES - 13 and b["x"] < curses.COLS - 3:
				screen[b["y"] + i][b["x"]] = c
				screen[b["y"]][b["x"]] = " "
		if b["y"] < curses.LINES - 14:
			b["y"] += 1
		else:
			bars.remove(b)

