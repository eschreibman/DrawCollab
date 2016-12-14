import sys, socket, getch, select, time, getopt
from p2p_protocol_message import protocol_message
from drawing_board import board, position
import curses
from peer_to_peer import peer

#have to do pip install py-getch
#run program either python gameClient.py or pythong gameClient.py -p portnum
#where portnum is the port number you wish to use (the server must use the same port number)

def getInput(stdscr):
        char = stdscr.getch()
        if char == -1:
                return -1
        #q quits the program
        if(char == ord("q")):
                print "Quiting..."
                shutdown_client()
                sys.exit();
                #server.close() #uncomment
        return char

def posDelta(dir):
        p = position(0, 0)
        if (dir == ord("w") or dir == curses.KEY_UP):
                p.updatePos(-1, 0)
        elif (dir == ord("s") or dir == curses.KEY_DOWN):
                p.updatePos(1, 0)
        elif (dir == ord("d") or dir == curses.KEY_RIGHT):
                p.updatePos(0, 1)
        elif (dir == ord("a") or dir == curses.KEY_LEFT):
                p.updatePos(0, -1)
        return p

#print to the curses string all the board characters with spaces in between
def printBoardClient(canvas, stdscr):
        k = 0; l = 0;
        for i in range(canvas.height):
                k = 0
                for j in range(canvas.width):
                        if(canvas.theboard[i][j] == canvas.user):
                                stdscr.addstr(l, k, canvas.theboard[i][j], curses.color_pair((canvas.userNum % 4) + 1))
                        else:
                                stdscr.addstr(l, k, canvas.theboard[i][j])
                        k += 2
                l += 1
                
def startScreen(canvas, stdscr):
        stdscr.addstr(0, 0, "Welcome!", curses.color_pair(2))
        stdscr.addstr(1, 0, "Use 'wasd' or arrow keys to move. Press 'q' to quit.", curses.color_pair(2))
        stdscr.addstr(3, 0, "Press any key to begin!", curses.color_pair(2))
        while(getInput(stdscr) == -1):
                continue
        stdscr.clear()

# def usage():
#     print "-p PORT_NUMBER, port to run server on (defaults to 9071)"
        
def debugMsg(str, offset, stdscr):
        j = (offset % 10) + 8
        for i in range(len(str)):
                if(i > 20):
                        j += 1
                        return
                stdscr.addstr(j, i, str[i])

def main(stdscr, portNum):
        
        port = portNum

        in_p2p_mode = False
        
        # try:
        #         options, args = getopt.getopt(sys.argv[1:], 'p:')
        #         port_selection = filter(lambda x: "-p" in x, options)
        #         if len(port_selection) > 0:
        #                 port = int(port_selection[0][1])
        # except (getopt.GetoptError, IndexError):
        #         usage()
        #         return()
        
        #curses set up
        curses.noecho()
        curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.curs_set(0)
        stdscr.nodelay(True)
        
        #server setup
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect(('127.0.0.1', port)) 

        peer_connections = [server]
        
        #send new user message
        dataString = "New User"
        dataSend = protocol_message(protocol_message.TYPE_NEW_USER, len(dataString), dataString)
        server.send(dataSend.collapsed())
        z = 0
        while True:
                if in_p2p_mode:
                        Connections, wlist, xlist = select.select([p2p_connection.connection()], [], [], 0.05)
                        for Connection in Connections:
                                Peer, info = Connection.accept()
                                peer_connections.append(Peer)

                read_list = []
                if not in_p2p_mode:
                        read_list = [server]
                else:
                        read_list = peer_connections
                 
                rlist, wlist, xlist = select.select(read_list, [], [], 0)
                for item in rlist: 
                        if item == server or True:
                                dataRec = item.recv(1024)
                                message_rec = protocol_message.message_from_collapsed(dataRec)
                                
                                if(message_rec.type == protocol_message.TYPE_WELCOME):
                                        #board set up
                                        userNum = message_rec.welcome_message_user_id()
                                        Height = 5
                                        Width = 10
                                        canvas = board(Width, Height) #TODO get width and height from server
                                        canvas.addUser(userNum)
                                        startScreen(canvas, stdscr)
                                        printBoardClient(canvas, stdscr)

                                if(message_rec.type == protocol_message.TYPE_UPDATE_BOARD):
                                        z += 1
                                        canvas.stringToBoardFromServer(message_rec.message)
                                        printBoardClient(canvas, stdscr)
                                        # if(canvas.stringToBoardFromServer(message_rec.message) == -1):
                                        #         debugMsg("error recv board", z, stdscr)
                                        #         z += 1
                                        #printBoardClient(canvas, stdscr)
                                        if in_p2p_mode:
                                                p2p_connection.forward_to_neighbors(message_rec)
                                if(message_rec.type == protocol_message.TYPE_P2P_NOTE):
                                        #in_p2p_mode = True
                                        p2p_connection = peer()
                                        server.send(p2p_connection.response_message().collapsed())
                                if(message_rec.type == protocol_message.TYPE_P2P_INFO):
                                        p2p_connection.add_neighbors(message_rec)
                                        in_p2p_mode = True
                        else:
                                dataRec = item.recv(1024)
                                        
                #get user input through the keyboard
                key = getInput(stdscr)
                if (key == -1):
                        continue
                
                if(key == ord("w") or key == ord("s") or key == ord("a") or key == ord("d") or key == curses.KEY_UP or key == curses.KEY_DOWN or key == curses.KEY_LEFT or key == curses.KEY_RIGHT):
                        #update our board and send it
                        newPos = posDelta(key)
                        canvas.moveUser(newPos)
                        boardString = canvas.boardToString()
                        message_send = protocol_message(protocol_message.TYPE_UPDATE_BOARD, len(boardString), boardString)
                        if not in_p2p_mode:
                                server.send(message_send.collapsed())
                        else:
                                p2p_connection.notify_neighbors(message_send)
                if(key == ord("p")):
                        #Request p2p mode
                        message_send = protocol_message(protocol_message.TYPE_P2P_REQUEST, 0, "")
                        server.send(message_send.collapsed())


#main for testing board logic without server
def main2():
        canvas = board(Width, Height)
        canvas.printBoard()
        while True:
                key = getch.getch()
                if(key == "q"):
                        print "Quiting..."
                        sys.exit()
                if(key == "w" or key == "s" or key == "a" or key == "d"):
                        newPos = posDelta(key)
                        canvas.moveUser(newPos)
                canvas.printBoard()


def shutdown_client():
        curses.echo()  
        curses.nocbreak()                                                                          
        curses.endwin()

def runP2P(portNum):
    curses.wrapper(main, portNum)

#when the program is run, call the above "main" function
# if __name__ == "__main__":
#         curses.wrapper(main)

