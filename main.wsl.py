import os
import curses
from curses import wrapper

HISTORY_LIMIT = 20
CMD_HISTORY = []
scroll_pos = 0

def main(stdscr):
	stdscr.clear()
	curses.echo()
	
	y_max,x_max = stdscr.getmaxyx()
	border = (y_max-3,x_max-2, 1,1)

	screen = curses.newwin(*border)
	y_max,x_max = screen.getmaxyx()
	screen.box()
	screen.refresh()

	pad = curses.newpad(y_max*3, x_max+10)
	pad.refresh(0,0, 2,2, y_max-1,x_max-1)

	while 1:
		cmd = myinput(pad, max_YX = (y_max-1,x_max-1), prompt = os.getcwd() + ": ", ac_list = os.listdir())

		if cmd == "ls":
			print(*os.listdir(), sep = '\n',end = "\n\n")
		
		elif cmd.startswith("cd"):
			path = cmd.split()[1]
			os.chdir(path)

		elif cmd == "exit":
			break

		elif cmd == "":
			pass

		else:
			screen.addstr("Invalid command: " + cmd + "\n")
			screen.refresh()
	

	pad.refresh()
	pad.getkey()

def myinput(win, y = None,x = None, max_YX = None, prompt = "",ac_list = []):
	global scroll_pos
	win.keypad(1)

	def safe_print(y=None,x=None,str=str):
		b,a = win.getyx()
		if x is None: x = a
		if y is None: y = b

		q,p = win.getmaxyx()
		if b >= q - 5:
			win.resize(q+max_YX[0],p)

		win.addstr(y,x,str)

	safe_print(y,x,prompt)

	inp = []
	i = h_i = 0
	res = ""
	temp_history = [0] + CMD_HISTORY
	flag = False

	def pad_refresh(no_scroll = True):
		global scroll_pos
		win.refresh(scroll_pos,0, 2,2, *max_YX)

		while not no_scroll and (curses.getsyx()[0] >= max_YX[0]-1):
			scroll_pos += 1
			win.refresh(scroll_pos,0, 2,2, *max_YX)

	def nav_cmd_stack(upIfTrue):
		nonlocal inp,i,h_i,temp_history
		temp_history[h_i] = "".join(inp)
				
		win.move(y,x-i)
		win.clrtoeol()
		pad_refresh()
		
		if upIfTrue: h_i += 1
		else: h_i -= 1

		inp = list(temp_history[h_i])
		i = len(inp)
		safe_print(str=temp_history[h_i])

	def handle_tab():
		nonlocal flag,i,inp

		res = "".join(inp)
		starts_with_res = []

		for line in ac_list:
			if line.startswith(res):
				starts_with_res.append(line)
		
		if len(starts_with_res) == 0:
			curses.beep()
			return

		# direct match
		if len(starts_with_res) == 1:
			win.move(y,x-i)
			win.clrtoeol()

			safe_print(str=starts_with_res[0])
			pad_refresh()

			inp.clear()
			inp = list(starts_with_res[0])
			i = len(inp)
			
			return

		else:
			temp_list = []
			idx = len(res)

			while True:
				ch = starts_with_res[0][idx]

				for line in starts_with_res:
					if line[idx] == ch:
						temp_list.append(line)
					
					# match for multiple values
					else:
						if flag:
							if len(starts_with_res) > 5:
								safe_print(y+2,0,"Show all  " + str(len(starts_with_res)) + " possibilities?  [y/n]: ")
								pad_refresh(no_scroll=False)
							while True:
								if len(starts_with_res) > 5:
									key = chr(win.getch())
								else: key = 'y'
									
								win.addch('\n')

								if key == 'y':
									for p in starts_with_res:
										safe_print(str = p + "\n")
										pad_refresh(no_scroll=False)
									
									safe_print(str="\n" + prompt + res)
									pad_refresh()
									break

								elif key == 'n':
									win.move(y+2,0)
									win.clrtoeol()

									win.move(y,x)
									pad_refresh()
									break
						
						flag = not flag
						return

				idx += 1

				# partial match
				if starts_with_res != temp_list:
					win.move(y,x-i)
					win.clrtoeol()

					safe_print(str=starts_with_res[0][:idx+1])
					pad_refresh()

					inp.clear()
					inp = list(starts_with_res[0][:idx+1])
					i = len(inp)
					
					return

	while 1:
		pad_refresh()
		c = win.getch()
		y,x = win.getyx()

		#Tab key
		if c == 9:
			handle_tab()

		elif c == curses.KEY_UP:
			if h_i < len(temp_history)-1:
				nav_cmd_stack(True)

		elif c == curses.KEY_DOWN:
			if h_i > 0:
				nav_cmd_stack(False)
				
		elif c == curses.KEY_LEFT:
			if i > 0:
				i -= 1
				win.move(y,x-1)

		elif c == curses.KEY_RIGHT:
			if i < len(inp):
				i += 1
				win.move(y,x+1)

		# DEL key
		elif c == curses.KEY_DC:
			if i < len(inp):
				inp.pop(i)
				win.delch(y,x)

		elif c == curses.KEY_BACKSPACE:
			if i > 0:
				inp.pop(i-1)
				i -= 1

				win.delch(y,x-1)
				win.move(y,x-1)
		
		elif c == curses.KEY_HOME:
			win.move(y,x-i)
			i = 0
		
		elif c == curses.KEY_END:
			win.move(y,(x + len(inp) - i))
			i = len(inp)
		
		elif c == curses.KEY_NPAGE:
			if scroll_pos < (win.getmaxyx()[0] - (max_YX[0] - 2)):
				scroll_pos += 1

		elif c == curses.KEY_PPAGE:
			if scroll_pos > 0:
				scroll_pos -= 1

		# Enter key
		elif c == 10:
			win.move(y+1,0)	
			pad_refresh()
			break

		elif chr(c).isprintable():
			if i < len(inp):
				win.insch(c)
				win.move(y,x+1)
			else:
				win.addch(c)
			inp.insert(i,chr(c))

			i += 1
	
	win.keypad(0)

	res = "".join(inp)

	if res != "":
		CMD_HISTORY.insert(0,res)
		if len(CMD_HISTORY) > 30: CMD_HISTORY.pop(0)

	return res

wrapper(main)
curses.endwin()
