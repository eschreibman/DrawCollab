class protocol_message:

        TYPE_NEW_USER = 0
        TYPE_WELCOME = 1
        TYPE_UPDATE_BOARD = 2
        TYPE_P2P_NOTE = 3
        TYPE_P2P_REQUEST = 4
        TYPE_P2P_RESPONSE = 5
        TYPE_P2P_INFO = 6
        
        SENTINEL = -1

        ADDR_SPACE = 16
        PORT_SPACE = 6
        NEIGHBOR_GAP = PORT_SPACE + ADDR_SPACE + 1
        
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

        
        @staticmethod
        def construct_peer_to_peer_info_data(neighbors):
                data = chr(len(neighbors))
                
                for neighbor in neighbors:
                        print neighbor
                        data += chr(len(neighbor['addr']))
                        data += str(neighbor['addr']).ljust(protocol_message.ADDR_SPACE)
                        data += str(neighbor['port']).ljust(protocol_message.PORT_SPACE)

                return data

        def peer_to_peer_note_num_neighbors(self):
                if self.type != protocol_message.TYPE_P2P_NOTE:
                        Exception.throw

                return ord(self.message[0])

        def peer_to_peer_note_neighbor_addr(self, neighbor):
                if self.type != protocol_message.TYPE_P2P_NOTE:
                        Exception.throw

                print neighbor
                addr_start_index = 1 + neighbor*protocol_message.NEIGHBOR_GAP + 1
                addr_end_index = ord(self.message[addr_start_index-1]) + addr_start_index
                return self.message[addr_start_index:addr_end_index]

        def peer_to_peer_note_neighbor_port(self, neighbor):
                if self.type != protocol_message.TYPE_P2P_NOTE:
                        Exception.throw

                start_port = 1+neighbor*protocol_message.NEIGHBOR_GAP+1+protocol_message.ADDR_SPACE
                end_port = start_port + protocol_message.PORT_SPACE
                return int(self.message[start_port:end_port])

        @staticmethod
        def construct_p2p_response_data(addr, port):
                data = str(addr).ljust(protocol_message.ADDR_SPACE)
                data += str(port).ljust(protocol_message.PORT_SPACE)

                return data

        def p2p_response_data_address(self):
                if self.type != protocol_message.TYPE_P2P_RESPONSE:
                        Exception.throw

                return self.message[0:protocol_message.ADDR_SPACE]

        def p2p_response_data_port(self):
                if self.type != protocol_message.TYPE_P2P_RESPONSE:
                        Exception.throw

                return self.message[protocol_message.ADDR_SPACE:protocol_message.ADDR_SPACE+protocol_message.PORT_SPACE]
