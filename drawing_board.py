import sys
from position_class import position
class board:
    def __init__(self, w, h, userNum):
        self.userNum = userNum
        if(userNum == 0):
            self.user = "^"
        elif(userNum == 1):
            self.user = "&"
        elif(userNum == 2):
            self.user = "%"
        else:
            self.user = "$"
        self.width = w
        self.height = h
        self.theboard = [['_' for x in range(w)] for y in range(h)]
        self.theboard[0][0] = "^"
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
        self.theboard[self.userPosition.x][self.userPosition.y] = self.user
    
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

    def stringToBoard(self, str):
        slen = len(str)
        #the string is not the correct size of the board
        if(slen < self.width * self.height):
            return -1
        k = 0
        for i in range(self.height):
                for j in range(self.width):
                        #don't include the delimiting characters
                        while(str[k] == "[" or str[k] == "," or str[k] == "]"):
                                k += 1
                        self.theboard[i][j] = str[k]
                        k += 1
        return 0




