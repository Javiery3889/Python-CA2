#!/usr/bin/env python3
import socket 
import signal
import sys
import os
import helper 
class uploadComm:
	def handleConnection(con,serverSocket):
		citydict = {}
		while True:
			buf = con.recv(4048)
			if len(buf) > 0:
			#Decode it to text
				if buf == b"N" or buf == b"s":
					continue
				else:
					print("Received from Client " +str(buf.decode()))
					errorflag = uploadComm.checkentry(buf,con,citydict)
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

class ReportComm:
	def printSummary(header,records):
		con.send("\n".encode())
		con.send(header.encode())
		con.send("\n".encode())
		con.send("{0}".format("="*47+"\n").encode())
		for rec in records:
		    con.send("{0:35s}{1:12.2f}\n".format(rec.name,rec.getSum()/100).encode())
		con.send("{0}".format("="*47).encode())
		con.send("\n".encode())

	def addSales(name,e,storeDic):
	    #check if the target city or the target category has been added to the dictionary.
	    #if not, add it now.
	    #update the sales total accordingly by using the addEntry() method.
	    if name in storeDic:
	        # existing record, retrieve it for sales update.
	        sData = storeDic[name]
	    else:
	        # create new SalesData object
	        sData = helper.SalesData(name,e) 
	    sData.addEntry(e)
	    storeDic[name]=sData 

	def process(itemDic, e, infp):
	    running_total = 0 # keep track of the total sales figure
	    #e = Entry() # get a new Entry object
	    lineNo=0
	    for line in infp:
	        line=line.strip()
	        lineNo+=1
	        e.verify(line) # load in the line (record) into the entry object 
	        if e.valid:
	            running_total += e.svalue
	            if lineNo % 10000 == 0: # print the running_total
	                print("Total Sales of the year is {0:10.2f} ".format(running_total/100),end="\r",flush=True)              
	            ReportComm.addSales(e.item,e,itemDic) # add to itemDic
	            # now write the current record to the corresponding file
	        else:
	            # Assumption - in part 1 - ignore invalid entry by skipping it.
	            # in part 2 of the assignment. The server program should terminate
	            # the client once it detects invalid entry upload.
	            pass
	    return running_total

	def handleConnection(con,serverSocket):
		files = os.listdir(path)
		citydict = {}
		while True:
			buf = con.recv(255)
			print(buf)
			if len(buf) > 0:
				#Decode it to text
				print("Received from Client " +str(buf.decode()))
				filename = str(buf.decode()) + ".txt"
				if buf == b"N" or buf == b"c":
					continue
				else:
					if filename in files:
						fp = open(os.path.join(path,filename))
						itemSales={} # key - item category, value - SalesData Object
						cur_entry=helper.Entry() # an Entry object, to be used by the process() 
						totalSales=0    
						# always clean up (remove) all existing file.
						totalSales=ReportComm.process(itemSales,cur_entry,fp)
						fp.close()
						    #now print the total sales
						print("Total Sales of the year is {0:10.2f} ".format(totalSales/100))
						
						con.send("Total Sales of the year is {0:10.2f}\n".format(totalSales/100).encode())
						    
						#now count and compute the sales of all the item categories.
						i=0
						i=len(list(itemSales.keys()))
						    
						con.send("The Average Sales From {1:4d} Item Categories:\n{0:47.2f}".format(totalSales/100/i,i).encode())

						#now print the top three and bottom three items (if there are more than 3 items)

						itemdata = list(itemSales.values())
						itemdata.sort(key=lambda x: x.getSum(),reverse=True)
						if len(itemdata)>3:
						    ReportComm.printSummary("Top Three Item Categories",itemdata[0:3])
						    ReportComm.printSummary("Bottom Three Item Categories",itemdata[-3:])
						else:
						    ReportComm.printSummary("Sales Figures by Item Categories",itemdata)
					else:
						con.sendall(b"Operation aborted due to invalid data.")
						break


			else: #client terminted
				return ""

		con.close()
		return buf.decode()


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
	signal.signal(signal.SIGINT, uploadComm.signal_handler)
	print("Waiting for a new client to connect")
	signal.signal(signal.SIGALRM, uploadComm.signal_handler)
	signal.alarm(10)
	#stays blocked until client has been accepted
	con, address = serverSocket.accept()
	SYN = con.recv(4048)
	if SYN == b's':
		con.sendall(b'k')
		print(uploadComm.handleConnection(con,serverSocket))
	elif SYN == b'c':
		con.sendall(b'k')
		print(ReportComm.handleConnection(con,serverSocket))

	

serverSocket.close()
print("Server Stopped")
