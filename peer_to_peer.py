from p2p_protocol_message import protocol_message

class p2p_mode:

    def __init__(self, peers):
        self.peers = []
        #For now just make an arbitrary ring
        for peer in peers:
            print peer['connection'].getpeername()
            
            self.peers.append(peer)
            self.peers[-1]['neighbors'] = []
            if len(self.peers) > 1:
                self.peers[-2]['neighbors'].append((peer['user_id'], peer['connection']))
                self.peers[-1]['neighbors'].append((self.peers[-2]['user_id'], self.peers[-2]['connection']))
        self.peers[0]['neighbors'].append((self.peers[-1]['user_id'], self.peers[-1]['connection']))
        self.peers[-1]['neighbors'].append((self.peers[0]['user_id'], self.peers[0]['connection']))
        self.print_peers()
    
    # Server functions

    # Assign peers

    # Notify users of peer to peer
    def send_peer_to_peer_notification(self):
        for peer in self.peers:
            dataSend = protocol_message.construct_peer_to_peer_notification_data(peer['neighbors'])
            message_send = protocol_message(protocol_message.TYPE_P2P_NOTE, len(dataSend), dataSend)        
            peer['connection'].send(message_send.collapsed())
            
    # Add a peer

    # Peer functions

    # Notify peers


        # Debugging/ printing
    def print_peers(self):
        if len(self.peers) <= 2:
            return
        for peer in self.peers:
            print "PEER"
            print "User ID: " + str(peer['user_id'])
            print "Neighbors: " + str(peer['neighbors'][0][0]) + " " + str(peer['neighbors'][1][0])
