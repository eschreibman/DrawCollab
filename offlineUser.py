import sys
from position_class import position
class user:
    def __init__(self, username, userID, position):
        self.name = username
        self.userID = userID
        self.pos = position

class userList:
	def __init__(self):
		self.theList = []

	def addNewUser(self, username, ID):
		p = position(0, 0)
		usr = user(username, ID, p)
		self.theList.append(usr)


	def updateUserPosition(self, usr, x, y):
		for i in self.theList:
			if(i.name == usr.name):
				i.pos.updatePos(x, y)

	def userExists(self, username):
		for i in self.theList:
			if(i.name == username):
				return True
		return False