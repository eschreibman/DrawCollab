#A server to run draw collab
import socket
import SimpleHTTPServer
import SocketServer
import getopt, sys

def main():
    
    port = 80
    host = "localhost"

    try:
        options, args = getopt.getopt(sys.argv[1:], 'p:')
        port_selection = filter(lambda x: "-p" in x, options)
        if len(port_selection) > 0:
            port = int(port_selection[0][1])
    except (getopt.GetoptError, IndexError):
        usage()
        return


    s = socket.socket()
    host = "localhost" #socket.gethostname()

    s.bind((host, port))
    s.listen(5)

    while True:
        c, addr = s.accept()
        print("Accepted a client")
        c.recv(1000)
        c.send("Welcome\n")
    
        while True:
            print c.recv(1000)
        #c.close()

def usage():
    print "-p PORT_NUMBER, port to run server on (defaults to 80)"

if __name__ == '__main__':
    main()
