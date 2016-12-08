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

        VISITED_SPACE = 20
        MESSAGE_OFFSET = VISITED_SPACE + 3
        DELIM = "-"
        
        def __init__(self, type, length, message):
                self.type = type
                self.length = length
                self.originator = 255
                self.message = message
                self.visited = []

        
        def update_originator(self, originator):
                self.originator = originator

        def add_visit(self, visited):
                self.visited.append(visited)
                
        @staticmethod
        def message_from_collapsed(collapsed_message):
                if(len(collapsed_message) != 0):
                        type = ord(collapsed_message[0])
                        length = ord(collapsed_message[1])
                        originator = ord(collapsed_message[2])
                        visited = eval(collapsed_message[3:protocol_message.MESSAGE_OFFSET])
                        message = collapsed_message[protocol_message.MESSAGE_OFFSET:]
                else:
                        type = protocol_message.SENTINEL
                        length = protocol_message.SENTINEL
                        originator = protocol_message.SENTINEL
                        message = protocol_message.SENTINEL
                        visited = []

                return_message = protocol_message(type, length, message)
                return_message.update_originator(originator)
                return_message.visited = visited
                return return_message


        def collapsed(self):
                collapsed_message = ""
                collapsed_message +=  chr(self.type)
                collapsed_message += chr(self.length)
                collapsed_message += chr(self.originator)
                collapsed_message += str(self.visited).ljust(protocol_message.VISITED_SPACE)
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
        def construct_peer_to_peer_info_data(neighbors, reciever_id):
                data = chr(len(neighbors))
                data += chr(reciever_id)
                
                for neighbor in neighbors:
                        print neighbor
                        data += chr(neighbor['user_id'])
                        data += str(neighbor['addr']).ljust(protocol_message.ADDR_SPACE)
                        data += str(neighbor['port']).ljust(protocol_message.PORT_SPACE)

                return data

        def peer_to_peer_info_num_neighbors(self):
                if self.type != protocol_message.TYPE_P2P_INFO:
                        Exception.throw

                return ord(self.message[0])

        def peer_to_peer_info_reciever_id(self):
                if self.type != protocol_message.TYPE_P2P_INFO:
                        Exception.throw
                return ord(self.message[1])

        def peer_to_peer_info_neighbor_addr(self, neighbor):
                if self.type != protocol_message.TYPE_P2P_INFO:
                        Exception.throw

                print neighbor
                addr_start_index = 2 + neighbor*protocol_message.NEIGHBOR_GAP + 1
                addr_end_index =  addr_start_index + protocol_message.ADDR_SPACE
                return self.message[addr_start_index:addr_end_index]

        def peer_to_peer_info_neighbor_port(self, neighbor):
                if self.type != protocol_message.TYPE_P2P_INFO:
                        Exception.throw

                start_port = 2+neighbor*protocol_message.NEIGHBOR_GAP+1+protocol_message.ADDR_SPACE
                end_port = start_port + protocol_message.PORT_SPACE
                return int(self.message[start_port:end_port])

        def peer_to_peer_info_neighbor_id(self, neighbor):
                if self.type != protocol_message.TYPE_P2P_INFO:
                        Exception.throw
                return ord(self.message[2+neighbor*protocol_message.NEIGHBOR_GAP])
        
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
