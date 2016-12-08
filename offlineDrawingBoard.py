import sys
from position_class import position
from offlineUser import user, userList
class board:
    possibleUsers = ["^", "&", "%", "$"]
    anyUser = "@"
    emptySpace = "_"

    def __init__(self, w, h):
        #create a totally empty board
        self.width = w
        self.height = h
        self.clearBoard()
        self.userPosition = position(0, 0)

    def addUser(self, userNum, userName):
        #called by client
        #add a user character and put it at the first spot in the board
        self.userNum = userNum
        self.userName = userName
        if(userNum < len(self.possibleUsers)):
            self.user = self.possibleUsers[userNum]
        else:
            self.user = self.possibleUsers[len(self.possibleUsers) - 1]
        self.theboard[self.userPosition.x][self.userPosition.y] = self.user
        
    def clearBoard(self):
        self.theboard = [[self.emptySpace for x in range(self.width)] for y in range(self.width)]

    def addUserServer(self):
        #called by server
        self.userNum = -1
        self.user = self.anyUser

    def printBoard(self):
        for i in range(self.height):
            for j in range(self.width):
                sys.stdout.write(self.theboard[i][j])
            print
        print

    #change self.userPosition and wrap around if needed, based on board size
    def moveUser(self, dir):
        val = 0
        oldPosX = self.userPosition.x
        oldPosY = self.userPosition.y
        #clear where the user cursor used to be
        #self.theboard[oldPosX][oldPosY] = self.emptySpace
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
    
    def update_user_token(self, user_token):
        self.user_token = user_token

    def updateBoardWithUserList(self, userList):
        i = 0
        for key, value in userList.theDictionary.items():
            i += 1
            self.updatePlayerPos(value.userID, value.pos)
        return i

    def updatePlayerPos(self, playerID, newPos):
        if(newPos.x >= self.height or newPos.x < 0):
            return -1
        if(newPos.y >= self.width or newPos.y < 0):
            return -1
        if(playerID < len(self.possibleUsers)):
            self.theboard[newPos.x][newPos.y] = self.possibleUsers[playerID]
        else:
            self.theboard[newPos.x][newPos.y] = self.anyUser




