import sys, socket, getch, select, time, getopt
from protocol_message import protocol_message
from drawing_board import board, position
import curses

#have to do pip install py-getch

Height = 5
Width = 10
userPos = position(0, 0)

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
                        if(canvas.theboard[i][j] == "^"):
                                stdscr.addstr(l, k, canvas.theboard[i][j], curses.color_pair(1))
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

def usage():
    print "-p PORT_NUMBER, port to run server on (defaults to 9071)"
        
def main(stdscr):
        
        port = 9071
    
        try:
                options, args = getopt.getopt(sys.argv[1:], 'p:')
                port_selection = filter(lambda x: "-p" in x, options)
                if len(port_selection) > 0:
                        port = int(port_selection[0][1])
        except (getopt.GetoptError, IndexError):
                usage()
                return()
        
        #curses set up
        curses.noecho()
        curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.curs_set(0)
        stdscr.nodelay(True)
        #board set up
        canvas = board(Width, Height)

        startScreen(canvas, stdscr)
        printBoardClient(canvas, stdscr)

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect(('127.0.0.1', port)) 
        
        boardString = canvas.boardToString()
        dataString = "New User"
        dataSend = protocol_message(protocol_message.TYPE_NEW_USER, len(dataString), dataString)
        server.send(dataSend.collapsed())
        
        while True:
                rlist, wlist, xlist = select.select([server], [], [], 0)
                for item in rlist: 
                        if item == server:
                                #stdscr.clear()
                                #stdscr.addstr(1,0, "in item is server")
                                dataRec = server.recv(1024)
                                message_rec = protocol_message.message_from_collapsed(dataRec)
                                #stdscr.addstr(2,0, message_rec.message)

                key = getInput(stdscr)
                if (key == -1):
                        continue
                #stdscr.addstr(0, 0, "key is " + key)
                
                if(key == ord("w") or key == ord("s") or key == ord("a") or key == ord("d") or key == curses.KEY_UP or key == curses.KEY_DOWN or key == curses.KEY_LEFT or key == curses.KEY_RIGHT):
                        #stdscr.addstr(3, 0, "sending new board")
                        newPos = posDelta(key)
                        canvas.moveUser(newPos)
                        printBoardClient(canvas, stdscr)
                        boardString = canvas.boardToString()
                        message_send = protocol_message(protocol_message.TYPE_UPDATE_BOARD, len(boardString), boardString)
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

#when the program is run, call the above "main" function
if __name__ == "__main__":
        curses.wrapper(main)

