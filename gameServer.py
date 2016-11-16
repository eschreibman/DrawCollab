import sys, socket, select, pickle
from protocol_message import protocol_message

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
server.bind(('', 9071))
print 'Socket bind complete'
server.listen(5)
print "Socket now listening"

posBoard = "[1]"
clients = []
while True:
    Connections, wlist, xlist = select.select([server], [], [], 0.05)

    for Connection in Connections:
        client, Informations = Connection.accept()
        clients.append(client)

    clientsList = []
    try:
        clientsList, wlist, xlist = select.select(clients, [], [], 0.05)
    except select.error:
        pass
    else:
        for clientInList in clientsList:
            dataRec = clientInList.recv(1024)
            #data = pickle.loads(data)
            print "Got: "
            print dataRec
            message = protocol_message.message_from_collapsed(dataRec)
            if(message.type == protocol_message.TYPE_NEW_USER):
                print "In new user"
                #print dataRec 
                dataSend = "Welcome. Use 'wasd' to move"
                #data = pickle.dumps(data)
                clientInList.send(dataSend)
            if(dataRec == "Updated board"):
                newBoard = clientInList.recv(1024)
                print(newBoard)
                dataSend = "New board"
                #data = pickle.dumps(data)
                clientInList.send(dataSend)
                clientInList.send(newBoard)
                

clientInList.close()
server.close()
