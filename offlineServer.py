import sys, socket, select, getopt
from offlineProtocol import protocol_message
from offlineDrawingBoard import board, position
from offlineUser import user, userList

#run program either python gameSever.py or pythong gameServer.py -p portnum
#where portnum is the port number you wish to use (the clients must use the same port number)


def notify_all_clients(clients, message):
    for client in clients:
        client.send(message.collapsed())

def usage():
    print "-p PORT_NUMBER, port to run server on (defaults to 9071)"


def main():
    port = getPort()
    #socket setup
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(('', port))
    except socket.error:
        print "Address already in use...quitting"
        exit()
    server.listen(5)

    clients = []
    message_id = 0

    client_info_list = []
    masterClientList = userList()
    offlineClientList = userList()
    num_users = 0

    while True:
        try:
            Connections, wlist, xlist = select.select([server], [], [], 0.05)
        except (select.error, KeyboardInterrupt):
            print "\nQuitting..."
            exit()
        
        for Connection in Connections:
            client, Informations = Connection.accept()
            clients.append(client)
           
        clientsList = []
        try:
            clientsList, wlist, xlist = select.select(clients, [], [], 0.05)
        except (select.error, KeyboardInterrupt):
            print "\nQuitting..."
            exit()
        else:
            for clientInList in clientsList:
                dataRec = clientInList.recv(1024)
                message_rec = protocol_message.message_from_collapsed(dataRec)
                if(message_rec.type == protocol_message.TYPE_USER_JOIN):
                    
                    username = message_rec.message
                    print "user " + username + " joined"
                    #have we seen this client before
                    if(offlineClientList.userExists(username)):
                        print "welcome back " + username + " with ID " + str(masterClientList.getUserNum(username))
                        masterClientList.addOrUpdateUser(offlineClientList.getUserByName(username))
                        offlineClientList.removeUser(username)
                        dataSend = masterClientList.listToString()
                        print "master list: " + dataSend
                        message_send = protocol_message(protocol_message.TYPE_WELCOME_BACK, protocol_message.SERVER, len(dataSend), dataSend)
                    else:
                        print "never before seen client " + username + "...assigned ID " + str(num_users)
                        #add new user to the list and associate their name with a user num
                        masterClientList.addUserDefault(username, num_users)
                        num_users += 1
                        dataSend = masterClientList.listToString()
                        print "master list: " + dataSend
                        message_send = protocol_message(protocol_message.TYPE_WELCOME_NEW, protocol_message.SERVER, len(dataSend), dataSend)

                    clientInList.send(message_send.collapsed())

                if(message_rec.type == protocol_message.TYPE_CLIENT_UPDATE_POS):
                    #a client updated their position
                    msgFromUser = user()
                    msgFromUser.fromString(message_rec.message)
                    masterClientList.addOrUpdateUser(msgFromUser)
                    #now send the updated client list out
                    dataSend = masterClientList.listToString()
                    print "master list: " + dataSend
                    message_send = protocol_message(protocol_message.TYPE_SERVER_UPDATE_POS, protocol_message.SERVER, len(dataSend), dataSend)
                    notify_all_clients(clients, message_send)

                if(message_rec.type == protocol_message.SENTINEL):
                    print "Client left"
                    clients.remove(clientInList)

                if(message_rec.type == protocol_message.TYPE_CLIENT_EXIT):
                    tempusr = user()
                    tempusr = masterClientList.getUserByID(message_rec.user)
                    print "Client " + tempusr.name + " left gracefully"
                    offlineClientList.addOrUpdateUser(tempusr)
                    masterClientList.removeUser(tempusr.name)
                    clients.remove(clientInList)

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
