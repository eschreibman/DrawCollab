import socket

s = socket.socket()
host = "localhost" #socket.gethostname()
port = 80

s.bind((host, port))
f = open('index.html', 'rb')
s.listen(5)

while True:
    c, addr = s.accept()
    print("Accepted a client")
    c.send("HTTP/1.1 200 OK \n Content-type:text/html \n\n")
    data = f.read(1024)
    while data != "":
        c.send(data)
        data = f.read(1024)
    f.seek(0,0)
