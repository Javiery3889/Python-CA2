# !/usr/bin/env python3
import socket 
import signal
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
		# if len(buf) > 0:
		# 	#Decode it to text
		# 	print("Received from Client " +str(buf.decode()))
		# 	con.sendall(b"k")

		# else: #client terminted
		try:
			buf = con.recv(2048)
			mesg = my_input(str(buf.decode()))
			serverSocket.settimeout(TIMEOUT)
			connected=True
			if len(buf) > 0:
			#Decode it to text
				print("Received from Client " +str(buf.decode()))
				con.sendall(b"k")
			elif mesg == None:
				print("Timeout")
				serverSocket.close()
				print("Server Stopped")
				break
		except Exception as inst:
			if str(inst) == "timed out":
				print("Connection time out")
			else:            
				if connected:
					print("Connection has been broken")
				else:
					print("Failed to connect")

	con.close()
	return buf.decode()

#Main 
serverSocket = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('127.0.0.1', 8091))


#max 5 connections 
serverSocket.listen(5)

while True:
	print("Waiting for a new client to connect")
	#stays blocked until client has been accepted
	con, address = serverSocket.accept()
	print(handleConnection(con,serverSocket))

	

serverSocket.close()
print("Server Stopped")