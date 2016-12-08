import sys, socket, getch, select, time, getopt
from offlineProtocol import protocol_message
from offlineDrawingBoard import board, position
from offlineUser import user, userList
import curses
import random

#have to do pip install py-getch
#run program either python gameClient.py or pythong gameClient.py -p portnum
#where portnum is the port number you wish to use (the server must use the same port number)


def getPort():
    port = 9071
    try:
        options, args = getopt.getopt(sys.argv[1:], 'p:')
        port_selection = filter(lambda x: "-p" in x, options)
        if len(port_selection) > 0:
            port = (int(port_selection[0][1]))
    except (getopt.GetoptError, IndexError):
        print "-p PORT_NUMBER, port to run server on (defaults to 9071)"
        exit()
    return port

def cursesInit():
        #curses set up
        curses.noecho()
        curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.curs_set(0)      

def getInput(stdscr):
        char = stdscr.getch()
        if char == -1:
                return -1
        #q quits the program
        if(char == ord("q")):
                exitmsg = "Quiting...goodbye!"
                shutdown_client(exitmsg)
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
def printBoardClient(canvas, myUserList, stdscr):
    canvas.clearBoard()
    canvas.updateBoardWithUserList(myUserList)
    k = 0; l = 0;
    for i in range(canvas.height):
        k = 0
        for j in range(canvas.width):
            if(canvas.theboard[i][j] == canvas.user):
                stdscr.addstr(l, k, canvas.theboard[i][j], curses.color_pair(canvas.userNum + 1))
            else:
                stdscr.addstr(l, k, canvas.theboard[i][j])
            k += 2
        l += 1
                
def startScreen(stdscr):
    stdscr.addstr(0, 0, "Welcome!", curses.color_pair(2))
    stdscr.addstr(1, 0, "Enter your username by typing and hit enter when done", curses.color_pair(2))
    stdscr.addstr(2, 0, "No whitespace allowed", curses.color_pair(2))
    name = getUserInputedName(stdscr)
    stdscr.clear()
    stdscr.addstr(0, 0, "Use 'wasd' or arrow keys to move. Press 'q' to quit.", curses.color_pair(2))
    stdscr.addstr(1, 0, "Press any key to begin!", curses.color_pair(2))
    while(getInput(stdscr) == -1):
            continue
    stdscr.clear()
    return name


def getUserInputedName(stdscr):
    i = 0
    usernameEntered = ""
    maxy, maxx = stdscr.getmaxyx()
    inpt = stdscr.getch()
    while((inpt != curses.KEY_DOWN) and (str(inpt) != "10") and (str(inpt) != "13")):
        #until the user hits enter
        if(inpt != -1):
            if(i >= maxx):
                #stop if the player goes off the window size limit
                break
            if(inpt == curses.KEY_BACKSPACE or str(inpt) == "127"):
                #allow users to use backspace
                if(i > 0):
                    i -= 1
                    usernameEntered = usernameEntered[:-1]
                    stdscr.addstr(3, i, " ", curses.color_pair(2))
            else:
                #adding to name
                if(str(inpt) != "32"):
                    #no whitespace
                    stdscr.addstr(3, i, chr(inpt), curses.color_pair(2))
                    usernameEntered += chr(inpt)
                    i += 1
        inpt = stdscr.getch()
    return usernameEntered

def userInitialization(clientName, myUserList, canvas):
    #get our assigned userID num from the list
    # print "in user init, the current user list: "
    # print(myUserList.listToString())
    assignedID = myUserList.getUserNum(clientName)
    #get the initial information about our name, ID, and pos
    userSelf = myUserList.getUserByName(clientName)
    canvas.addUser(assignedID, clientName)
    # print "end of user init, the current user list: "
    # print(myUserList.listToString())
    return userSelf

        
def main(stdscr):
    global z
    z = 0 #DEBUG
    port = getPort()

    #server setup
    global server 
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    cursesInit()
    stdscr.nodelay(True)
    clientName = startScreen(stdscr)
    #board setup
    Height = 5
    Width = 10
    canvas = board(Width, Height)

    #user and userlist setup
    myUserList = userList()
    userSelf = user()
    userSelf.updateUsername(clientName)

    try:
        server.connect(('127.0.0.1', port))
    except socket.error as msg:
        exitmsg = "Unable to connect to port " + str(port) + "...quiting."
        shutdown_client(exitmsg)
        
     
    
    #send new user message, sends the username and 0 as the id
    dataSend = protocol_message(protocol_message.TYPE_USER_JOIN, 0, len(clientName), clientName)
    server.send(dataSend.collapsed())
    
    
    
    while True:
        try:
            rlist, wlist, xlist = select.select([server], [], [], 0)
        except socket.error as msg:
            exitmsg = "Select failed...quiting."
            shutdown_client(exitmsg)
        for item in rlist: 
                if item == server:
                    try:
                        dataRec = server.recv(1024)
                    except socket.error as msg:
                        exitmsg = "Connection reset by peer...quiting."
                        shutdown_client(exitmsg)
                    
                    message_rec = protocol_message.message_from_collapsed(dataRec)
                    
                    if(message_rec.type == protocol_message.TYPE_WELCOME_NEW):
                        debugMsg("welcome new", stdscr)
                        
                        #populate the userlist with information from the server
                        myUserList.stringToUserList(message_rec.message)
                        userSelf = userInitialization(clientName, myUserList, canvas)
                        debugMsg("init user " + userSelf.toString(), stdscr)
                        debugMsg("user list " + myUserList.listToString(), stdscr)
                        printBoardClient(canvas, myUserList, stdscr)
                        # debugMsg("end of welcome new", stdscr)
                        # debugMsg(userSelf.toString(), stdscr)

                    if(message_rec.type == protocol_message.TYPE_WELCOME_BACK):
                        debugMsg("welcome back", stdscr)
                        #populate the userlist with information from the server
                        myUserList.stringToUserList(message_rec.message)
                        userSelf = userInitialization(clientName, myUserList, canvas)
                        debugMsg("init user " + userSelf.toString(), stdscr)
                        debugMsg("user list " + myUserList.listToString(), stdscr)
                        printBoardClient(canvas, myUserList, stdscr)
                
                    if(message_rec.type == protocol_message.TYPE_SERVER_UPDATE_POS):
                        debugMsg("server update pos", stdscr)
                        #debugMsg(message_rec.message, stdscr)
                        val = myUserList.stringToUserList(message_rec.message)
                        # debugmsg = myUserList.listToString()
                        
                        printBoardClient(canvas, myUserList, stdscr)
                        # debugMsg(debugmsg, stdscr)
                        # debugMsg(str(x), stdscr)
                        # debugMsg(str(val), stdscr)
                                    
        #get user input through the keyboard
        key = getInput(stdscr)
       
        if(key == ord("w") or key == ord("s") or key == ord("a") or key == ord("d") or key == curses.KEY_UP or key == curses.KEY_DOWN or key == curses.KEY_LEFT or key == curses.KEY_RIGHT):
            #update our position and send it
            # debugMsg("user self top of kat fnc", stdscr)
            # debugMsg(userSelf.toString(), stdscr)
            newPos = posDelta(key)
            canvas.moveUser(newPos)
            userSelf.pos = canvas.userPosition
            posToSend = userSelf.toString()
            # debugMsg("user self position to send", stdscr)
            # debugMsg(posToSend, stdscr)
            message_send = protocol_message(protocol_message.TYPE_CLIENT_UPDATE_POS, userSelf.userID, len(posToSend), posToSend)
            server.send(message_send.collapsed())

# def main():
#     global z
#     z = 0 #DEBUG
#     port = getPort()

#     #server setup
#     global server 
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#     # cursesInit()
#     # stdscr.nodelay(True)
#     # clientName = startScreen(stdscr)
#     clientName = random.choice("abcdefghijklmnopqrstuvwxyz")
#     print "client name: " + clientName
#     #board setup
#     Height = 5
#     Width = 10
#     canvas = board(Width, Height)

#     #user and userlist setup
#     myUserList = userList()
#     userSelf = user()
#     userSelf.updateUsername(clientName)

#     try:
#         server.connect(('127.0.0.1', port))
#     except socket.error as msg:
#         exitmsg = "Unable to connect to port " + str(port) + "...quiting."
#         # shutdown_client(exitmsg)
        
     
    
#     #send new user message, sends the username and 0 as the id
#     dataSend = protocol_message(protocol_message.TYPE_USER_JOIN, 0, len(clientName), clientName)
#     server.send(dataSend.collapsed())
    
    
    
#     while True:
#         try:
#             rlist, wlist, xlist = select.select([server], [], [], 0)
#         except socket.error as msg:
#             exitmsg = "Select failed...quiting."
#             # shutdown_client(exitmsg)
#         for item in rlist: 
#                 if item == server:
#                     try:
#                         dataRec = server.recv(1024)
#                     except socket.error as msg:
#                         exitmsg = "Connection reset by peer...quiting."
#                         # shutdown_client(exitmsg)
                    
#                     message_rec = protocol_message.message_from_collapsed(dataRec)
                    
#                     if(message_rec.type == protocol_message.TYPE_WELCOME_NEW):
#                         # debugMsg("welcome new", stdscr)
#                         print("welcome new")
#                         #populate the userlist with information from the server
#                         myUserList.stringToUserList(message_rec.message)
#                         userSelf = userInitialization(clientName, myUserList, canvas)
#                         posToSend = userSelf.toString()
#                         print "user at end of welcome " + posToSend
#                         # printBoardClient(canvas, stdscr)
#                         # debugMsg("end of welcome new", stdscr)
#                         # debugMsg(userSelf.toString(), stdscr)

#                     if(message_rec.type == protocol_message.TYPE_WELCOME_BACK):
#                         # debugMsg("welcome back", stdscr)
#                         #populate the userlist with information from the server
#                         myUserList.stringToUserList(message_rec.message)
#                         userInitialization(clientName, myUserList, canvas)
#                         # printBoardClient(canvas, stdscr)
                
#                     if(message_rec.type == protocol_message.TYPE_SERVER_UPDATE_POS):
#                         # debugMsg("server update pos", stdscr)
#                         #debugMsg(message_rec.message, stdscr)
#                         print("update board pos")
#                         val = myUserList.stringToUserList(message_rec.message)
#                         debugmsg = myUserList.listToString()
#                         canvas.clearBoard()
#                         x = canvas.updateBoardWithUserList(myUserList)
#                         #printBoardClient(canvas, stdscr)
#                         # debugMsg(debugmsg, stdscr)
#                         # debugMsg(str(x), stdscr)
#                         # debugMsg(str(val), stdscr)
                                    
#         #get user input through the keyboard
#         # key = getInput(stdscr)
#         key = raw_input("Please enter something: ")
       
#         #if(key == ord("w") or key == ord("s") or key == ord("a") or key == ord("d") ):# or key == curses.KEY_UP or key == curses.KEY_DOWN or key == curses.KEY_LEFT or key == curses.KEY_RIGHT):
#         if(key == "w" or key == "s" or key == "a" or key == "d"):
#             #update our position and send it
#             # debugMsg("user self top of kat fnc", stdscr)
#             # debugMsg(userSelf.toString(), stdscr)
#             print "got wasd"
#             newPos = posDelta(key)
#             canvas.moveUser(newPos)
#             userSelf.pos = canvas.userPosition
#             posToSend = userSelf.toString()
#             print "string sent to server: " + posToSend
#             # debugMsg("user self position to send", stdscr)
#             # debugMsg(posToSend, stdscr)
#             message_send = protocol_message(protocol_message.TYPE_CLIENT_UPDATE_POS, userSelf.userID, len(posToSend), posToSend)
#             server.send(message_send.collapsed())
#         if(key == "q"):
#             exit()



def shutdown_client(exitMessage):
        curses.echo()  
        curses.nocbreak()                                                                          
        curses.endwin()
        #close the socket connected to the server
        server.close()
        print exitMessage
        exit()

def debugMsg(str, stdscr):
    global z
    j = (z % 8) + 5
    for i in range(len(str)):
        if(i > 30):
            z += 1
            return
        stdscr.addstr(j, i, str[i])
    z += 1

#when the program is run, call the above "main" function
if __name__ == "__main__": #main()
        curses.wrapper(main)

