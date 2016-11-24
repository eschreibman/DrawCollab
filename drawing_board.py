import sys
from position_class import position
class board:
    possibleUsers = ["^", "&", "%", "$"]
    anyUser = "@"

    def __init__(self, w, h):
        #create a totally empty board
        self.width = w
        self.height = h
        self.theboard = [['_' for x in range(w)] for y in range(h)]

    def addUser(self, userNum):
        #called by client
        #add a user character and put it at the first spot in the board
        self.userNum = userNum
        if(userNum < len(self.possibleUsers)):
            self.user = self.possibleUsers[userNum]
        else:
            self.user = self.possibleUsers[len(self.possibleUsers) - 1]
        self.theboard[0][0] = self.user
        self.userPosition = position(0, 0)

    def printBoard(self):
        for i in range(self.height):
            for j in range(self.width):
                sys.stdout.write(self.theboard[i][j])
            print
        print

    def moveUser(self, dir):
        val = 0
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
            val = -1
        elif(self.userPosition.x == self.height):
            self.userPosition.x = 0
            val = -2
        #wrap around y
        if(self.userPosition.y < 0):
            self.userPosition.y = self.width - 1
            val = -3
        elif(self.userPosition.y == self.width):
            self.userPosition.y = 0
            val = -4

        #update user position on board
        self.theboard[self.userPosition.x][self.userPosition.y] = self.user
        return val
    
    def boardToString(self):
        string = ""
        for i in range(self.height):
            string += "["
            #width one less time to not put a comma at the end
            for j in range(self.width - 1):
                string += self.theboard[i][j]
                string += ","
            string += self.theboard[i][self.width - 1]
            string += "]"
        return string

    def stringToBoardFromServer(self, str):
        slen = len(str)
        k = 0
        for i in range(self.height):
                for j in range(self.width):
                        #don't include the delimiting characters
                        while(str[k] == "[" or str[k] == "," or str[k] == "]"):
                                k += 1
                        #deal with two users being on the same spot
                        # if(str[k] == self.anyUser):
                        #     self.theboard[i][j] = self.user
                        if(k == slen):
                            return -1
                        self.theboard[i][j] = str[k]
                        k += 1
        return 0

    
    def update_user_token(self, user_token):
        self.user_token = user_token
