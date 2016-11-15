import socket, select, pickle

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
server.bind(('', 9070))
print 'Socket bind complete'
server.listen(5)
print "Socket now listening"

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
            data = clientInList.recv(1024)
            #data = pickle.loads(data)
            if(data == "I'm logged"):
                print(data)
                data = "Welcome"
                #data = pickle.dumps(data)
                clientInList.send(data)

clientInList.close()
server.close()