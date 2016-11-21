import sys
from position_class import position
class board:
        
	def __init__(self, w, h):
		self.width = w
		self.height = h
		self.theboard = [['_' for x in range(w)] for y in range(h)]
                self.user_token = '^'
		self.theboard[0][0] = self.user_token
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
		self.theboard[oldPosX][oldPosY] = '_'
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
		self.theboard[self.userPosition.x][self.userPosition.y] = self.user_token
	
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

        def update_user_token(self, user_token):
                self.user_token = user_token
