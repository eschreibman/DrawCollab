import sys, socket, getch, select
from protocol_message import protocol_message
import curses

#have to do pip install py-getch

#################################  CLASSES START  ##############################################

class position:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def updatePos(self, x, y):
		self.x = x
		self.y = y



class board:
	def __init__(self, w, h):
		self.width = w
		self.height = h
		self.theboard = [[' _ ' for x in range(w)] for y in range(h)]
		self.theboard[0][0] = " ^ "
		self.userPosition = position(0, 0)

	def printBoard(self):
		for i in range(self.height):
			for j in range(self.width):
				sys.stdout.write(self.theboard[i][j])
			print
		print

	def moveUser(self, dir):
		oldPosX = self.userPosition.x
		oldPosY = self.userPosition.y
		#clear where the user cursor used to be
		self.theboard[oldPosX][oldPosY] = ' _ '
		#update user position
		self.userPosition.x += dir.x
		self.userPosition.y += dir.y
		#wrap around x
		if(self.userPosition.x < 0):
			self.userPosition.x = self.height - 1
		elif(self.userPosition.x == self.height):
			self.userPosition.x = 0
		#wrap around y
		if(self.userPosition.y < 0):
			self.userPosition.y = self.width - 1
		elif(self.userPosition.y == self.width):
			self.userPosition.y = 0

		#update user position on board
		self.theboard[self.userPosition.x][self.userPosition.y] = " ^ "
	
	def boardToString(self):
		string = ""
		for i in range(self.height):
			string += "["
			for j in range(self.width - 1):
				string += self.theboard[i][j]
				string += ","
			string += self.theboard[i][j]
			string += "]"
		return string


#################################  CLASSES END  ##############################################

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

