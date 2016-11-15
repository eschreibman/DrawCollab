import socket, pickle

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(('127.0.0.1', 9070))
while True:
    dataSend = "I'm logged"
    #data = pickle.dumps(data)
    server.send(dataSend)
    dataRec = server.recv(1024)
    if(dataRec == "Welcome"):
	    #data = pickle.loads(data)
	    print(dataRec)
	    bg.update()
server.close()
