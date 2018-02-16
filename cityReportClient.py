#!/usr/bin/env python3
# source file: simClient.py

import socket
SYN = 'c'
def getNewSocket():
    return socket.socket( socket.AF_INET, \
        socket.SOCK_STREAM)

# Main program starts here

# Establish a connectin with Server
# running same machine, we use port = 8089
clientSocket = getNewSocket()
host = "localhost"
clientSocket.connect((host,8091)) #Must be same as port used by Server

# Allow Client to keep sending messages
# to server until client decide to quit
clientSocket.send(b'c')
if clientSocket.recv(1) == b"k":
    while True:
        msg = input("msg to send ['q' to quit; 'x' to quit and stop the server]=> ")

        # Convert msg to bytes
        obuf = msg.encode()

        #send that message to server
        clientSocket.send(obuf)

        # Check whether to quit or not 
        if (msg == 'q' or msg == 'x'):
            clientSocket.close()
            break
        else:
            # We expect Server to echo back the 
            # mesage that we just send
            ibuf = clientSocket.recv(2048)
            if len(ibuf) > 0:
                print("Server Echo "+ibuf.decode())
            else:
                print("The connection has been terminated")
                break

print("Bye")
