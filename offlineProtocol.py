class protocol_message:

        TYPE_USER_JOIN = 0
        TYPE_WELCOME_NEW = 1
        TYPE_WELCOME_BACK = 2
        TYPE_USER_JOIN = 3
        TYPE_CLIENT_UPDATE_POS = 4
        TYPE_SERVER_UPDATE_POS = 5
        TYPE_CLIENT_EXIT = 6
        SERVER = 0

        SENTINEL = -1
        
        def __init__(self, type, user, length, message):
                self.type = type
                #who the message is sent from, is 0 for the server or new user
                self.user = user
                self.length = length
                self.message = message

        @staticmethod
        def message_from_collapsed(collapsed_message):
                if(len(collapsed_message) != 0):
                        type = ord(collapsed_message[0])
                        user = ord(collapsed_message[1])
                        length = ord(collapsed_message[2])
                        message = collapsed_message[3:]
                else:
                        type = protocol_message.SENTINEL
                        user = protocol_message.SENTINEL
                        length = protocol_message.SENTINEL
                        message = protocol_message.SENTINEL
                return protocol_message(type, user, length, message)


        def collapsed(self):
                collapsed_message = ""
                collapsed_message +=  chr(self.type)
                collapsed_message +=  chr(self.user)
                collapsed_message += chr(self.length)
                collapsed_message = collapsed_message + self.message
                return collapsed_message
