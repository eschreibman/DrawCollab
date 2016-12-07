from p2p_protocol_message import protocol_message
import socket

class p2p_mode:

    def __init__(self, peers):
        print "in p2p init"
        self.peers = []
        #For now just make an arbitrary ring
        for peer in peers:
            print peer['connection'].getpeername()
            
            self.peers.append(peer)
            self.peers[-1]['neighbors'] = []
            if len(self.peers) > 1:
                neighbor_data = {'user_id':peer['user_id']}
                self.peers[-2]['neighbors'].append(neighbor_data.copy())
                self.peers[-1]['neighbors'].append(self.peers[-2])
        self.peers[0]['neighbors'].append(self.peers[-1])
        self.peers[-1]['neighbors'].append(self.peers[0])

        self.total_peers = len(self.peers)
        self.total_responded = 0
        
        self.print_peers()
    
    # Server functions
    def add_connection_data(self, connection):
        self.total_responded += 1
        for peer in self.peers:
            for neighbor in peer['neighbors']:
                if neighbor['user_id'] == connection['user_id']:
                    neighbor['addr'] = connection['addr']
                    neighbor['port'] = connection['port']

        print "total_peers " + str(self.total_peers) + " total_responded " + str(self.total_responded)

    def ready(self):
        return self.total_peers == self.total_responded
    # Assign peers

    # Notify users of peer to peer
    def send_peer_to_peer_notification(self):
        print "sending p2p note"
        for peer in self.peers:
            message_send = protocol_message(protocol_message.TYPE_P2P_NOTE, 0, "")
            peer['connection'].send(message_send.collapsed())
            
    def send_peer_to_peer_info(self):
        for peer in self.peers:
            dataSend = protocol_message.construct_peer_to_peer_info_data(peer['neighbors'])
            message_send = protocol_message(protocol_message.TYPE_P2P_INFO, len(dataSend), dataSend)        
            peer['connection'].send(message_send.collapsed())
            
    # Add a peer


    # Debugging/ printing
    def print_peers(self):
        if len(self.peers) <= 2:
            return
        for peer in self.peers:
            print "PEER"
            print "User ID: " + str(peer['user_id'])
            print "Neighbors: " + str(peer['neighbors'][0]['user_id']) + " " + str(peer['neighbors'][1]['user_id'])

class peer:

    def __init__(self):
        self.peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.peer.bind(('', 0))
        self.peer.listen(5)

    def response_message(self):
        dataSend = protocol_message.construct_p2p_response_data(self.peer.getsockname()[0], self.peer.getsockname()[1])
        message_send = protocol_message(protocol_message.TYPE_P2P_RESPONSE, len(dataSend), dataSend)
        return message_send
