from offlineClient import *
from p2p_gameClient import *

def usage():
    print "[-oP] [-p PORT_NUMBER]" 
    print " -o for offline mode, -P for peer to peer mode, -p with desired port number to run server on"

def main():
    port = 9071
    try:
        options, args = getopt.getopt(sys.argv[1:], 'oPp:')
        if(len(sys.argv) != 4):
            usage()
            exit()

        port_selection = filter(lambda x: "-p" in x, options)
        peerToPeerMode = filter(lambda x: "-P" in x, options)
        offlineMode = filter(lambda x: "-o" in x, options)
        if (len(port_selection) > 0):
            port = (int(port_selection[0][1]))
        if (not offlineMode):
            if(not peerToPeerMode):
                usage()
                exit()
            else:
                print "Running peer to peer mode..."
                runP2P(port)
        else:
            print "Running in offline mode..."
            runOffline(port)
        
    except (getopt.GetoptError, IndexError, ValueError):
        usage()
        exit()


#when the program is run, call the above "main" function
if __name__ == "__main__": main()