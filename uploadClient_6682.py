#!/usr/bin/env python3
#source file: uploadClient.py
#Sample program for AY20172018 S2 PYC Assignment 2. Part II.
import socket
import sys
import os,time
import signal
TIMEOUT=10
BUFSIZ=225
PORT_NO=8091
ACK = "k"
NO_MORE_UPLOAD= "N"
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
def printnow():
    print(time.ctime()[0:19])
def getnewsocket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def myopenf(filename):
    try:
        fp = open(filename,"r")
        return fp
    except: # catch all errors
        return None
def printUsage(cmdpath):
    cmds = os.path.split(cmdpath)
    print("Usage: {0} <sales data file>".format(cmds[1]))


# main program flow starts here
def wait_then_send(client_sock, wait_for, send_this):
    # Enter here when the client program is ready to send a message to the server
    # It will wait for an acknowledgement message (ie. 'k') then will proceed to send.
    try:
        #excepting a 'wait_for' message as acknowledgement  
        ibuf = client_sock.recv(BUFSIZ)
        if len(ibuf) > 0:
            ack=ibuf.decode()     
        else:
            #recevied empty str, it implies the connection has been dropped.
            #print("The connection has dropped")
            return "The connection has dropped"
        if ack==wait_for:
            msg = send_this
            #print("sending {0}".format(msg))
            obuf = msg.encode() # convert msg string to bytes
            ret=client_sock.sendall(obuf)
            return None  # return None implies wait_and_send is successful.
        else:
            # The ack is the expected acknowledge. It must be an error
            # message. Return the message to the caller.
            return ack
    except Exception as inst:
            return "Something wrong. Has to drop the connection"
def startnow(server_addr,fp):
    #print(server_addr)
    printnow()
    uploadcount=0  # will increment for receiving the subsequent
                   # corresponding ack.
    clientsocket = getnewsocket()
    connected=False
    normalExit=True
    try:
        clientsocket.connect(server_addr)
        clientsocket.settimeout(TIMEOUT)
        msg="s" 
        connected=True
        obuf = msg.encode() # convert msg string to bytes
        ret=clientsocket.sendall(obuf) # send out an initial 's'.
        for line in fp: # start the main wait_and_send loop.
            #excepting a 'k' as acknowledgement
            reply=wait_then_send(clientsocket,ACK,line.strip())
            if reply != None: # something wrong
                print(reply)
                normalExit = False
                break
            uploadcount+=1      # successfully sent out one more sales record.
            if uploadcount % 100 == 0:
                print("Entries Uploaded: {0:6d}".format(uploadcount),end="\r")
        #exit from the loop
        if normalExit:
            #Reach here because of end of file
            #expecting one more 'k' as acknowledgement  
            reply=wait_then_send(clientsocket,ACK,NO_MORE_UPLOAD)
            if reply != None: # something wrong
                print(reply)
                normalExit = False
        if normalExit:
            print("Entries Uploaded: {0:6d}".format(uploadcount))
        else:    
            print("Uploading Operation has been aborted.\nPlease try again.") 
        clientsocket.close()
    except Exception as inst:
        if str(inst) == "timed out":
            print("Connection time out")
        else:            
            if connected:
                print("Connection has been broken")
            else:
                print("Failed to connect")
    if connected:
        clientsocket.close()
    fp.close()
    printnow()
def main(fp):
        # ask for server address before the starting the game.
    choice=""
    while not choice in ['l','c','q']:
        choice = my_input("Server type ? [l]an , [c]loud or [e]xit =>",defval="e")
        if choice == 'l':
            startnow(('127.0.0.1', PORT_NO),fp)
        elif choice == 'c':
            startnow(('dmit2.bulletplus.com',80),fp)      
        elif choice == 'e':
            fp.close()
            return
#main program starts here.
if len(sys.argv) != 2:
    printUsage(sys.argv[0])
    sys.exit(-1)
else:
    fname=sys.argv[1]
fp = myopenf(fname)
if fp == None:
    print("Invalid data file. Operation aborted.")
    sys.exit(-2)
main(fp)
print("See You again.")