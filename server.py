# Initial server goals:
#   Accept requests
#   Server infomation

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
            port = port_selection[0][1]
    except (getopt.GetoptError, IndexError):
        usage()
        return

    handler = SimpleHTTPServer.SimpleHTTPRequestHandler # TODO make actual request handler
    server = SocketServer.TCPServer((host, port), handler)

    server.serve_forever()

    return

def usage():
    print "-p PORT_NUMBER, port to run server on (defaults to 80)"

if __name__ == '__main__':
    main()
