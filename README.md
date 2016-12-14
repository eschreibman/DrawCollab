# DrawCollab
Networks final project

## Concept
Our original concept for this assignment was for a drawing collaboration application. What we have ended up completing is more similar to a game where users can move characters around a board. We decided to focus on the networking aspects and give up some of our hopes for the front-end drawing aspect of the project. Because of this we have two different, separate, and robust modes that you can run this program in. One is the “offline mode” where users can log in with a user name and a server will communicate all the client positions to each of the clients currently online. If a client logs off or goes into “offline mode” their last state will be saved while other users can change their states. The other mode is that of a peer to peer network where users can move their characters around and those states are communicated via their peers with no server as a middle-man. 


## Modules

### Offline Mode
To run server 'python Server.py -p <port> -o'
To run client 'python Client.py -p <port> -o'
You may need to run 'pip install py-getch' to run the client

### Offline Mode Test Case
The “offline mode” was created to mimic the way that current online collaboration documents allow you to keep track of your state of changes even if you exit the program. Additionally, when you come back into the program you begin where you last left off and if changes by other users happened while you were offline they are now shown. Some ways to use this mode/test cases are:
In all the following cases the first step is to close any server that was previously running and start running the server again (so all the tests start with a new server) 
*Begin by running one client. You must “log in” with a username. You can move your “character” around the “board”
*You can run one client, move around, quit the program using “q” and then start the client again with the same username. You will see your character where you last left it
*You can run multiple clients (with unique usernames). You can move each of them around and their new position will be reflected on all the clients’ screens.
*While running multiple clients if one client quits using “q” their character will disappear from all other clients’ screens. If they “log back in” they should reappear in the last place they were at on all screens
*While running multiple clients (or just one) you can go into offline mode by pressing “o” and then move the character around. This simulates losing connection to the server but still wanting to make changes that are noted locally and then when you go back online (by hitting “o” again) your position and all the other client positions are updated 


### Peer to peer mode
To run server 'python Server.py -p <port> -P'
To run client 'python Client.py -p <port> -P'

### Peer to Peer Mode Test Case
The peer to to peer mode exists to allow the users to exist independantly from the server. To run the peer to peer mode at least three users must be logged into the server. To test the peer to peer mode do the following:
*Start the server running with the Server.py program with the -P flag
*Connect at least three clients to the server
*Once all clients are connected any client can initiate peer to peer mode by pressing 'p'
*Once this has been done the server will put all clients in peer to peer mode
*At this point the server can be closed and the peers with continue to operate together
