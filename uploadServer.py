#!/usr/bin/env python3
import socket 
import signal
import sys
import os
import shutil

def handleConnection(con,serverSocket):
	connected=False
	normalExit=True
	citydict = {}
	while True:
		buf = con.recv(4048)
		if len(buf) > 0:
		#Decode it to text
			if buf == b"N" or buf == b"s":
				con.sendall(b"k")
				continue
			else:
				print("Received from Client " +str(buf.decode()))
				errorflag = checkentry(buf,con,citydict)
				if errorflag is True:
					con.sendall(b"Operation aborted due to invalid data.")
					break
				con.sendall(b"k")
		else:
			return ""
	con.close()
	return buf.decode()

def checkentry(buf,con,citydict):
	decodedmsg = buf.decode()
	error = False
	splitmsg = decodedmsg.split("\t")
	if len(splitmsg) == 6:
		try:
			citydict[splitmsg[2]]=float(splitmsg[4])
		except ValueError:
			error = True
		if len(citydict) != 1:
			error = True
			shutil.rmtree(path)

		else:
			filepath = os.path.join(path,splitmsg[2]) 
			with open(filepath+".txt","a") as fp:
				fp.write(decodedmsg + "\n")
				
	else:
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
currentwd = os.getcwd() 
path = currentwd + "/salesRecords"
if os.path.isdir(path) is False:
	os.mkdir(path)

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
