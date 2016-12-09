import sys
from position_class import position
class user:
    def __init__(self):
        self.name = ""
        self.userID = 0
        self.pos = position(0, 0)

    def setNameIDPos(self, username, userID, position):
        self.name = username
        self.userID = userID
        self.pos = position

    def updateUsername(self, username):
        self.name = username

    def updateID(self, userID):
        self.userID = userID

    def updatePosition(self, position):
        self.pos = position

    def toString(self):
        string = self.name
        string += " "
        string += str(self.userID)
        string += " "
        string += self.pos.toString()
        return string

    def fromString(self, string):
        #print "in from string, got string: " + string
        try:
            self.name, ID, x, y = string.split(" ")
            self.userID = int(ID)
            self.pos.updatePos(int(x), int(y))
        except ValueError:
            self.manualParse(string)
    
    #error handling for if a client sends a string too long
    #such as in the case where they move too quickly (keyboard input is too fast) and two sends become one message
    def manualParse(self, string):
        i = 0
        numelm = 0
        strlen = len(string)
        tempstr = ""
        while(i < strlen):
            if(ord(string[i]) == 0 or ord(string[i]) == 4):
                break
            tempstr += string[i]
            i += 1

        self.name, ID, x, y = tempstr.split(" ")
        self.userID = int(ID)
        self.pos.updatePos(int(x), int(y))


        

class userList:
    def __init__(self):
        #assumes unique user names!
        self.theDictionary = {}

    def addOrUpdateUser(self, usr):
        self.theDictionary[usr.name] = usr

    def addUserDefault(self, username, ID):
        p = position(0, 0)
        usr = user()
        usr.setNameIDPos(username, ID, p)
        self.theDictionary[username] = usr

    def addUserWithPosition(self, username, ID, x, y):
        p = position(x, y)
        usr = user()
        usr.setNameIDPos(username, ID, p)
        self.theDictionary[username] = usr

    def updateUserPosition(self, usr, x, y):
        if(usr.name in self.theDictionary):
            self.theDictionary[usr.name].pos.updatePos(x, y)

    def updateUserPos(self, usr, position):
        if(usr.name in self.theDictionary):
            self.theDictionary[usr.name].pos = position

    def userExists(self, username):
        if(username in self.theDictionary):
            return True
        return False

    def getUserNum(self, username):
        if(username in self.theDictionary):
            return self.theDictionary[username].userID

    def getUserPos(self, username):
        if(username in self.theDictionary):
            return self.theDictionary[username].pos

    def getUserByName(self, username):
        if(username in self.theDictionary):
            return self.theDictionary[username]

    def getUserByID(self, ID):
         for key, value in self.theDictionary.items():
            if(ID == value.userID):
                return value

    def updatePosByID(self, ID, pos):
        for key, value in self.theDictionary.items():
            if(ID == value.userID):
                value.pos = pos
                break


    #return the list of users (represented by their names, ids, and positions)
    #ex: [eliza 1 0 0][nicki 2 1 3]
    def listToString(self):
        string = ""
        #for i in self.theList:
        for key, value in self.theDictionary.items():
            string += "["
            string += value.toString()
            string += "]"
        return string

    def stringToUserList(self, str):
        self.theDictionary.clear()
        strlen = len(str)
        i = 0; val = 0;
        while(i < strlen):
            oneUser = ""; username = ""; ID = ""; x = ""; y = ""
            if(str[i] != "["):
                while(str[i] != "]"):
                    oneUser += str[i]
                    i += 1
                tempusr = user()
                if(tempusr.fromString(oneUser) == -1):
                    val = -1
                self.addOrUpdateUser(tempusr)
            i += 1
        return val

    def printList(self):
        for keys,values in self.theDictionary.items():
            print(keys)
            print(values.name)
            print(str(values.userID))
            print(str(values.pos.toString()))

    def removeUser(self, username):
        self.theDictionary.pop(username, None)
                

 

