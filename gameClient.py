import sys, socket, getch, select
from protocol_message import protocol_message
from drawing_board import board, position
import curses

#have to do pip install py-getch

Height = 5
Width = 10
userPos = position(0, 0)

def getInput(stdscr):
	char = stdscr.getch()
	if char == -1:
		return -1
	#q quits the program
	if(char == ord("q")):
		print "Quiting..."
		shutdown_client()
		sys.exit();
		#server.close() #uncomment
	return chr(char) 

def posDelta(dir):
	p = position(0, 0)
	if (dir == "w"):
		p.updatePos(-1, 0)
	elif (dir == "s"):
		p.updatePos(1, 0)
	elif (dir == "d"):
		p.updatePos(0, 1)
	elif (dir == "a"):
		p.updatePos(0, -1)
	return p

def printBoardClient(canvas, stdscr):
	k = 0; l = 0;
	for i in range(canvas.height):
		for j in range(canvas.width):
			stdscr.addstr(l, k, canvas.theboard[i][j])
		k += 2
	l += 1
		

def main(stdscr):
	curses.noecho()
	stdscr.nodelay(True)
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.connect(('127.0.0.1', 9071)) 
	canvas = board(Width, Height)
	boardString = canvas.boardToString()
	dataString = "New User"
	dataSend = protocol_message(protocol_message.TYPE_NEW_USER, len(dataString), dataString)
	server.send(dataSend.collapsed())
	stdscr.clear()
	while True:
		rlist, wlist, xlist = select.select([server], [], [], 0)
		for item in rlist: 
			if item == server:
                                #stdscr.clear()
		                #stdscr.addstr(1,0, "in item is server")
				dataRec = server.recv(1024)
				message_rec = protocol_message.message_from_collapsed(dataRec)
				#stdscr.addstr(2,0, message_rec.message)

                key = getInput(stdscr)
                if (key == -1):
                        continue
                #stdscr.addstr(0, 0, "key is " + key)
                
		if(key == "w" or key == "s" or key == "a" or key == "d"):
			#stdscr.addstr(3, 0, "sending new board")
			newPos = posDelta(key)
			canvas.moveUser(newPos)
			printBoardClient(canvas, stdscr)
			boardString = canvas.boardToString()
			message_send = protocol_message(protocol_message.TYPE_UPDATE_BOARD, len(boardString), boardString)
			server.send(message_send.collapsed())


def main2():
	canvas = board(Width, Height)
	canvas.printBoard()
	while True:
		key = getch.getch()
		if(key == "q"):
			print "Quiting..."
			sys.exit()
		if(key == "w" or key == "s" or key == "a" or key == "d"):
			newPos = posDelta(key)
			canvas.moveUser(newPos)
		canvas.printBoard()


def shutdown_client():
	curses.echo()  
	curses.nocbreak()                                                                          
	curses.endwin()

#when the program is run, call the above "main" function
if __name__ == "__main__": main2()
	#curses.wrapper(main)

