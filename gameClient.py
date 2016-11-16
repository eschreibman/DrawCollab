import sys, socket, pickle, getch
from protocol_message import protocol_message
from drawing_board import board

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

def getInput():
	char = getch.getch()
	#q quits the program
	if(char == "q"):
		print "Quiting..."
		sys.exit();
		#server.close() #uncomment
	return char

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

def main():
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print "Socket created"
	server.connect(('127.0.0.1', 9071)) 
	print "Socket connected"
	canvas = board(Width, Height)
	boardString = canvas.boardToString()
	stringToBoardPrint(boardString);
	while True:
		dataString = "New User"
		dataSend = protocol_message(protocol_message.TYPE_NEW_USER, len(dataString), dataString)
		#data = pickle.dumps(data)
		server.send(dataSend.collapsed())
		dataRec = server.recv(1024)
		print "Data rec: " + dataRec 
		message_rec = protocol_message.message_from_collapsed(dataRec)
		if(message_rec.type == protocol_message.TYPE_WELCOME):
			#data = pickle.loads(data)
			message_send = protocol_message(protocol_message.TYPE_UPDATE_BOARD, len(boardString), boardString)
			server.send(message_send.collapsed())
			dataRec = server.recv(1024)
			print(dataRec)
			break

def main2():
	#canvas = board(Width, Height)
	#canvas.printBoard()
	while True:
		key = getInput()
		if(key == "w" or key == "s" or key == "a" or key == "d"):
			newPos = posDelta(key)
			canvas.moveUser(newPos)
		canvas.printBoard()



#when the program is run, call the above "main" function
if __name__ == "__main__": main()

