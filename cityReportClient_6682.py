#!/usr/bin/env python3
# source file: simClient.py

import socket
import sys
import os,time
import signal
PORT_NO = 8091
TIMEOUT = 10
SYN = 'c'
def getNewSocket():
    return socket.socket( socket.AF_INET, \
        socket.SOCK_STREAM)
def printnow():
    print(time.ctime()[0:19])
def interrupted(signum, frame):
    # a signal triggered function,
    #it raises a ValueError once it is triggered.
    raise ValueError("interrupted")
    #print ("interrupted")
def my_input(prompt,tm=TIMEOUT,defval=None):
    #my_input is a user defined function to provide a keyboard input
    #function with additonal timeout feature.
    #When the timeout interval is due, this function will return a default value
    #even there is no keyboard input.
    signal.signal(signal.SIGALRM, interrupted) # define the alarm handler
    signal.alarm(int(tm))   #start an alarm count down. default is 10 seconds
    try:
        data = input(prompt)
        signal.alarm(0) # Keyboard input is entered. clear the alarm
        if data == '':
            data=defval
        return data
    except:
        # timeout
        return defval  

# Main program starts here

# Establish a connectin with Server
# running same machine, we use port = 8089
def startnow(server_ip):
    printnow()
    clientSocket = getNewSocket()
    clientSocket.connect(server_ip) #Must be same as port used by Server
    file = sys.argv[1]
    # Allow Client to keep sending messages
    # to server until client decide to quit
    clientSocket.send(b'c')
    filename = sys.argv[1]
    if clientSocket.recv(1) == b"k":
        clientSocket.send(file.encode())
        while True:
            #send that message to server

            # We expect Server to echo back the 
            # mesage that we just send
            ibuf = clientSocket.recv(2048)
            if len(ibuf) > 0:
                print(ibuf.decode())
            else:
                print("The connection has been terminated")
                clientSocket.close()
                break
        clientSocket.close()
    printnow()
def main():
        # ask for server address before the starting the game.
    choice=""
    while not choice in ['l','c','q']:
        choice = my_input("Server type ? [l]an , [c]loud or [e]xit =>",defval="e")
        if choice == 'l':
            startnow(('127.0.0.1', PORT_NO))
        elif choice == 'c':
            startnow(('dmit2.bulletplus.com',80))      
        elif choice == 'e':
            sys.exit()
            return
#main program starts here.
if len(sys.argv) != 2:
    printUsage(sys.argv[0])
    sys.exit(-1)
main()
print("See You again.")