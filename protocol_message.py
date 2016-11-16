class protocol_message:

    TYPE_NEW_USER = 0
    TYPE_UPDATE_BOARD = 1

    def __init__(self, type, length, message):
        self.type = type
        self.length = length
        self.message = message

    def __init__(self, collapsed_message):
        self.type = ord(collapsed_message[0])
        self.length = ord(collapsed_message[1])
        self.message = collapsed_message[2:]


    def collapsed(self):
        collapsed_message[0] = chr(self.type)
        collapsed_message[1] = chr(self.length)
        collapsed_message = collapsed_message + self.message
