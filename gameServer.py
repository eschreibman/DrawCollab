import sys, socket, select, getopt
from protocol_message import protocol_message
from drawing_board import board

def notify_all_clients(clients, message):
    print("Notifying all clients")
    for client in clients:
        client.send(message.collapsed())

def usage():
    print "-p PORT_NUMBER, port to run server on (defaults to 9071)"


port = 9071
    
try:
    options, args = getopt.getopt(sys.argv[1:], 'p:')
    port_selection = filter(lambda x: "-p" in x, options)
    if len(port_selection) > 0:
        port = int(port_selection[0][1])
except (getopt.GetoptError, IndexError):
    usage()
    exit()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
server.bind(('', port))
print 'Socket bind complete'
server.listen(5)

print "Socket now listening"
    
posBoard = "[1]"
clients = []
message_id = 0
while True:
    Connections, wlist, xlist = select.select([server], [], [], 0.05)
    
    for Connection in Connections:
        client, Informations = Connection.accept()
        clients.append(client)
        print clients
        
    clientsList = []
    try:
        clientsList, wlist, xlist = select.select(clients, [], [], 0.05)
    except select.error:
        pass
    else:
        for clientInList in clientsList:
            dataRec = clientInList.recv(1024)
            print "Got: "
            print dataRec
            message_rec = protocol_message.message_from_collapsed(dataRec)
            if(message_rec.type == protocol_message.TYPE_NEW_USER):
                dataSend = "Welcome. Use 'wasd' to move"
                message_send = protocol_message(protocol_message.TYPE_WELCOME, len(dataSend), dataSend)
                clientInList.send(message_send.collapsed())
            if(message_rec.type == protocol_message.TYPE_UPDATE_BOARD):
                print(message_rec.message)
                dataSend = "New board" + str(message_id)
                message_id += 1
                message_send = protocol_message(protocol_message.TYPE_UPDATE_BOARD, len(dataSend), dataSend)
                clientInList.send(message_send.collapsed())
                notify_all_clients(clients, message_send)
            if(message_rec.type == protocol_message.SENTINEL):
                clients.remove(clientInList)
                # TODO add this client to a waiting to be reconnected list
clientInList.close()
server.close()
