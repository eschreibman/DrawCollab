import sys, socket, getch, select
from protocol_message import protocol_message
from drawing_board import board
import curses


#have to do pip install py-getch

class position:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def updatePos(self, x, y):
		self.x = x
		self.y = y


Height = 5
Width = 10
userPos = position(0, 0)

def getInput(stdscr):
	char = stdscr.getch()
	if char == -1:
		return -1
	#q quits the program
	if(char == "q"):
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

def stringToBoardPrint(string):
	strlen = len(string)
	for i in range(strlen):
		if(string[i] == '_' or string[i] == "^" or string[i] == " "):
			sys.stdout.write(string[i])
		elif(string[i] == "]"):
			print

def main(stdscr):
	curses.echo()
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print "Socket created"
	server.connect(('127.0.0.1', 9071)) 
	print "Socket connected"
	canvas = board(Width, Height)
	boardString = canvas.boardToString()
	dataString = "New User"
	dataSend = protocol_message(protocol_message.TYPE_NEW_USER, len(dataString), dataString)
	server.send(dataSend.collapsed())
	while True:
		rlist, wlist, xlist = select.select([server], [], [])
		key = getInput(stdscr)
		stdscr.addstr(0, 0, "key is " + key)
		if(key == "w" or key == "s" or key == "a" or key == "d"):
			newPos = posDelta(key)
			canvas.moveUser(newPos)
			canvas.printBoard()
			boardString = canvas.boardToString()
			message_send = protocol_message(protocol_message.TYPE_UPDATE_BOARD, len(boardString), boardString)
			server.send(message_send.collapsed())

		for item in rlist: 
			if item == server:
				print "in item is server"
				dataRec = server.recv(1024)
				message_rec = protocol_message.message_from_collapsed(dataRec)
				print message_rec.message

def shutdown_client():
	curses.echo()                                                                                                                                                                                   
	curses.nocbreak()                                                                                                                                                                                  
	curses.endwin()

#when the program is run, call the above "main" function
if __name__ == "__main__": 
	curses.wrapper(main)

