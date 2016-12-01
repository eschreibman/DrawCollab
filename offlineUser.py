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

    def addUserDefault(self, username, ID):
        p = position(0, 0)
        usr = user(username, ID, p)
        self.theList.append(usr)

    def addUserWithPosition(self, username, ID, x, y):
        p = position(x, y)
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

    def getUserNum(self, username):
        for i in self.theList:
            if(i.name == username):
                return i.userID

        return -1

    #return the list of users (represented by their names, ids, and positions)
    #ex: [eliza 1 0 0][nicki 2 1 3]
    def listToString(self):
        string = ""
        for i in self.theList:
            string += "["
            string += i.name
            string += " "
            string += str(i.userID)
            string += " "
            string += str(i.pos.x)
            string += " "
            string += str(i.pos.y)
            string += "]"
        return string

    def stringToUserList(self, str):
        strlen = len(str)
        i = 0;
        while(i < strlen):
            oneUser = ""; username = ""; ID = ""; x = ""; y = ""
            if(str[i] == "["):
                i += 1
            else:
                while(str[i] != "]"):
                    oneUser += str[i]
                    i += 1
                username, ID, x, y = oneUser.split(" ")
                # i += 1 #ignore the white space
                # while(str[i] != " "):
                #     ID += str[i]
                #     i += 1
                # i += 1 #ignore the white space
                # while(str[i] != " "):
                #     x += str[i]
                #     i += 1
                # i += 1 #ignore the white space
                # while(str[i] != " "):
                #     y += str[i]
                #     i += 1
                i += 1
                self.addUserWithPosition(username, int(ID), int(x), int(y))
 

