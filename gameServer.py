import sys, socket, select, getopt
from offlineProtocol import protocol_message
from offlineDrawingBoard import board

#run program either python gameSever.py or pythong gameServer.py -p portnum
#where portnum is the port number you wish to use (the clients must use the same port number)

def notify_all_clients(clients, message):
    print("Notifying all clients")
    for client in clients:
        client.send(message.collapsed())

def usage():
    print "-p PORT_NUMBER, port to run server on (defaults to 9071)"


def main():
    port = getPort()
    #socket setup
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', port))
    server.listen(5)

    Height = 5
    Width = 10
    masterBoard = board(Width, Height)
    masterBoard.addUserServer()
    recvBoard = board(Width, Height)
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
                    masterBoard.addUser(client_info_list[user_id_index]['user_id'])

                if(message_rec.type == protocol_message.TYPE_CUR_BOARD):
                    curBoardState = protocol_message(protocol_message.TYPE_CUR_BOARD, len(masterBoard.boardToString()), masterBoard.boardToString())
                    clientInList.send(curBoardState.collapsed())
                    
                if(message_rec.type == protocol_message.TYPE_UPDATE_BOARD):
                    print("Got update board")
                    print(message_rec.message)
                    recvBoard.stringToBoard(message_rec.message)
                    recvBoard.findMyUser()
                    masterBoard.mergeBoards(recvBoard)
                    #send the board back
                    dataSend = masterBoard.boardToString()
                    message_send = protocol_message(protocol_message.TYPE_UPDATE_BOARD, len(dataSend), dataSend)
                    notify_all_clients(clients, message_send)
                if(message_rec.type == protocol_message.SENTINEL):
                    clients.remove(clientInList)
                    # TODO add this client to a waiting to be reconnected list
    clientInList.close()
    server.close()

#see if the user has run the program with a designated port number
#if not, set the default port number
def getPort():
    port = 9071
    try:
        options, args = getopt.getopt(sys.argv[1:], 'p:')
        port_selection = filter(lambda x: "-p" in x, options)
        if len(port_selection) > 0:
            port = (int(port_selection[0][1]))
    except (getopt.GetoptError, IndexError):
        usage()
        exit()
    return port


#when the program is run, call the above "main" function
if __name__ == "__main__": main()
