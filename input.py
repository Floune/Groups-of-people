import curses

def updateInputLine(buffer, txtBox):
	i = 1
	j = 1
	for char in buffer:
		if i > curses.COLS - 2:
			j += 1
			i = 1
		if len(buffer) < curses.COLS * 2 - 6:
			txtBox.addstr(j, i, char)
			i+=1

def waitInput(q, txtBox):
	buffer = []
	arrows = ["KEY_UP","KEY_DOWN","KEY_LEFT","KEY_RIGHT"]
	last = -1
	inp = ""
	while inp != "/quit":
		last = txtBox.getkey(2, 2)

		if last in arrows:
			buffer = []
			q.put(last)
		elif last == "KEY_BACKSPACE" and len(buffer) > 0:
			buffer.pop()
			txtBox.clear()
			txtBox.box()
			updateInputLine(buffer, txtBox)
			txtBox.refresh()
		elif last == '\n':
			inp = "".join(buffer)
			q.put(inp)
			buffer = []
		elif len(buffer) < curses.COLS * 2 - 6 and last != "KEY_BACKSPACE":
			buffer.append(last)
			updateInputLine(buffer, txtBox)
