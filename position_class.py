class position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def updatePos(self, x, y):
        self.x = x
        self.y = y

    def toString(self):
        string = ""
        string += str(self.x)
        string += " "
        string += str(self.y)
        return string

    def stringToPosition(self, string):
        self.x, self.y = string.split(" ")