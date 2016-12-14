import sys, socket, select, getopt
from p2p_protocol_message import protocol_message
from drawing_board import board
from peer_to_peer import p2p_mode

#run program either python gameSever.py or pythong gameServer.py -p portnum
#where portnum is the port number you wish to use (the clients must use the same port number)

def notify_all_clients(clients, message):
    print("Notifying all clients")
    for client in clients:
        client.send(message.collapsed())

def usage():
    print "-p PORT_NUMBER, port to run server on (defaults to 9071)"


def runP2P(portNum):
    port = portNum
        
    # try:
    #     options, args = getopt.getopt(sys.argv[1:], 'p:')
    #     port_selection = filter(lambda x: "-p" in x, options)
    #     if len(port_selection) > 0:
    #         port = int(port_selection[0][1])
    # except (getopt.GetoptError, IndexError):
    #     usage()
    #     exit()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'Socket created'

    server.bind(('', port))
    server.listen(5)

    Height = 5
    Width = 10
    masterBoard = board(Width, Height)
    clients = []
    message_id = 0
    
    client_info_list = []
    num_users = 0

    while True:
        Connections, wlist, xlist = select.select([server], [], [], 0.05)

        for Connection in Connections:
            client, Informations = Connection.accept()
            clients.append(client)
            client_info_list.append({'user_id': num_users, 'connection': client, 'connected': True})
            num_users += 1
            print clients
            # Test peer to peer mode init on every new client
            #print "P2P"
            #p2p_mode(client_info_list)

        clientsList = []
        try:
            clientsList, wlist, xlist = select.select(clients, [], [], 0.05)
        except select.error:
            pass
        else:
            for clientInList in clientsList:
                dataRec = clientInList.recv(1024)
                #print "Got: "
                #print dataRec
                message_rec = protocol_message.message_from_collapsed(dataRec)
                if(message_rec.type == protocol_message.TYPE_NEW_USER):
                    user_id_index = next(index for (index, d) in enumerate(client_info_list) if d['connection'] == clientInList)
                    print "User id:"
                    print client_info_list[user_id_index]['user_id']
                    dataSend = protocol_message.construct_welcome_message_data(client_info_list[user_id_index]['user_id'])
                    message_send = protocol_message(protocol_message.TYPE_WELCOME, len(dataSend), dataSend)
                    clientInList.send(message_send.collapsed())

                if(message_rec.type == protocol_message.TYPE_UPDATE_BOARD):
                    print("Got update board")
                    print(message_rec.message)
                    #send the board back
                    dataSend = message_rec.message
                    #message_id += 1
                    message_send = protocol_message(protocol_message.TYPE_UPDATE_BOARD, len(dataSend), dataSend)
                    notify_all_clients(clients, message_send)
                if(message_rec.type == protocol_message.SENTINEL):
                    clients.remove(clientInList)
                    # TODO add this client to a waiting to be reconnected list
                if(message_rec.type == protocol_message.TYPE_P2P_REQUEST):
                    p2p = p2p_mode(client_info_list)
                    p2p.send_peer_to_peer_notification()

                if(message_rec.type == protocol_message.TYPE_P2P_RESPONSE):
                    user_id_index = next(index for (index, d) in enumerate(client_info_list) if d['connection'] == clientInList)
                    connection = {}
                    connection['user_id'] = client_info_list[user_id_index]['user_id']
                    connection['addr'] = message_rec.p2p_response_data_address()
                    connection['port'] = message_rec.p2p_response_data_port()
                    p2p.add_connection_data(connection.copy())
                    if (p2p.ready()):
                        p2p.send_peer_to_peer_info()
                    
    clientInList.close()
    server.close()



# #when the program is run, call the above "main" function
# if __name__ == "__main__": main()
