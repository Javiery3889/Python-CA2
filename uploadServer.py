#!/usr/bin/env python3
import socket 
import signal
import sys
TIMEOUT=3
#function that deals with a client that is connected
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
        data = prompt
        signal.alarm(0) # Keyboard input is entered. clear the alarm
        if data == '':
            data=defval
        return data
    except:
        # timeout
        return defval  

def handleConnection(con,serverSocket):
	connected=False
	normalExit=True
	while True:
		buf = con.recv(2048)
		print("wdwd"+str(buf))
		if len(buf) > 0:
		#Decode it to text
			if buf != b"N" or buf != b"s":
				print("Received from Client " +str(buf.decode()))
				errorflag = checkentry(buf,con)
				if errorflag is True:
					con.sendall(b"Operation aborted due to invalid data.")
					break
				con.sendall(b"k")
		else:
			return ""
	con.close()
	return buf.decode()
def printerrormsg():
	
	return print("Operation aborted due to invalid data.\nUploading Operation has been aborted.\nPlease try again.\n")

def checkentry(buf,con):
	decodedmsg = buf.decode()
	error = False
	splitmsg = decodedmsg.split("\t")
	print(splitmsg)
	if len(splitmsg) == 6:
		try:
			float(splitmsg[4])
		except ValueError:
			error = True


	return error

def signal_handler(signal, frame):
	serverSocket.close()
	print("\nSocket Closed")
	sys.exit(0)

#Main 
serverSocket = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind(('127.0.0.1', 8091))


#max 5 connections 
serverSocket.listen(5)

while True:
	signal.signal(signal.SIGINT, signal_handler)
	print("Waiting for a new client to connect")
	signal.signal(signal.SIGALRM, signal_handler)
	signal.alarm(10)
	#stays blocked until client has been accepted
	con, address = serverSocket.accept()
	print(handleConnection(con,serverSocket))

	

serverSocket.close()
print("Server Stopped")
