# DrawCollab
Networks final project

## Concept

## Modules

### Peer to peer mode
To run server `python p2p_gameServer -p <port>`
To run client `python p2p_gameClient -p <port>`

The project also includes a basic peer to peer mode of operation. In this mode users join the project first by connecting to the server. Once all clients are present, any user can put everyone in peer to peer mode by pressing the 'p' key. This user sends a message to the server to initiate peer to peer mode. The server then notifies all clients with a peer to peer notification message. The clients each set up a server of their own and send their address and port number to the server. Once all clients have responded the server sends every client a message with the information about their neighbors. The users then connect to their peers, and all messages to the server cease.  

The peer to peer mode used in this project is very basic, the following are ways it could be improved in the future:
 * The current mode has no support for losing peers (once a peer drops out the other peers go down as soon as they try to contact the fallen node). In later iterations of this project 