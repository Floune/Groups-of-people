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
	txtBox.refresh()

def waitInput(q, txtBox):
	buffer = []
	last = -1
	inp = ""
	while inp != "/quit":
		last = txtBox.getkey(2, 2)
		if last == '\n':
			inp = "".join(buffer)
			q.put(inp)
			buffer = []
		# if last in self.arrows:
		#   q.put(last)
		elif len(buffer) < curses.COLS * 2 - 6:
			buffer.append(last)
			updateInputLine(buffer, txtBox)
