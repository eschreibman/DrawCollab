class protocol_message:

        TYPE_NEW_USER = 0
        TYPE_WELCOME = 1
        TYPE_UPDATE_BOARD = 2
        TYPE_CUR_BOARD = 3

        SENTINEL = -1
        
        def __init__(self, type, length, message):
                self.type = type
                self.length = length
                self.message = message

        @staticmethod
        def message_from_collapsed(collapsed_message):
                if(len(collapsed_message) != 0):
                        type = ord(collapsed_message[0])
                        length = ord(collapsed_message[1])
                        message = collapsed_message[2:]
                else:
                        type = protocol_message.SENTINEL
                        length = protocol_message.SENTINEL
                        message = protocol_message.SENTINEL
                return protocol_message(type, length, message)


        def collapsed(self):
                collapsed_message = ""
                collapsed_message +=  chr(self.type)
                collapsed_message += chr(self.length)
                collapsed_message = collapsed_message + self.message
                return collapsed_message


        @staticmethod
        def construct_welcome_message_data(user_id):
                welcome = ""
                welcome += chr(user_id)
                return welcome


        def welcome_message_user_id(self):
                if self.type != protocol_message.TYPE_WELCOME:
                        Exception.throw
                        #TODO make more specific exception

                return ord(self.message[0])
