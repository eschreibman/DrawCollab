class p2p_mode:

    def __init__(self, peers):
        self.peers = []
        #For now just make an arbitrary ring
        for peer in peers:
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
