#python file contains classes to suppor the AY20171018S2 PYC Python assignment
#
# Author : Karl
# Created : Nov 2017
# Last updated: Jan 2018
# Util class provide static methods for
#    printNow():
#    provides simple timestamp printing.
#    cleanFolder() and checkCreate() :
#    take in a directory name to do folder clean up and initialization
#    appendToFiles(), and closeAllFiles():
#    take in a common dictionary to maintain muliple opened files.
#
# Entry class supports the data abstraction for a sales record entry
#
# SalesData class supports the data abstraction for either a
# city sales summary or category sales summary

import os
import time

class Util:
    # declare the column positions
    dateCol=0
    timeCol=1
    cityCol=2
    itemCol=3
    salesCol=4
    paymentCol=5
    MAX_OPEN=120                 #default the maximum open files.
    repDir = 'reports'           #default Part 1 datafiles folder
    storeDir = 'serverStore'     #default Part 2 datafiles folder
    def printnow():
        print(time.ctime()[0:19])
        
    def cleanFolder(dir=repDir):
        # removing all existing files from the 'dir'
        for the_file in os.listdir(dir):
            file_path = os.path.join(dir, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                #print(e)
                pass
    def checkCreate(dir=storeDir,needtoclean=True):
        #function to ensure the 'dir' is existing.
        #if 'needtoclean' is True, all the content of the 'dir' will be remove.
        #default value of 'needtoclean' is set to True
        try:
            os.stat(dir)
            # need to clean up ?
            if needtoclean:
                Util.cleanFolder(dir)
        except:
            #reach here implies 'dir' does not exist.
            os.makedirs(dir)
    def closeAllFiles(fpDic):
        #close all the opened files, the file descriptors are storing
        # in the fpDic dictionary.
        for city in list(fpDic.keys()):
            fpDic[city].close()
            del fpDic[city]
    def appendToFile(city,line,fpDic,dir=repDir):
        #append a line of text to a file.
        #check if the file is already opened by search it from teh fpDic.
        #If not, then open it in append mode and store the file descriptor in
        #the fpDic dictionary.
        #If found it, use the stored file descriptor to write out the line.
        if city not in fpDic:
            # need to add a new element and open the file.
            if len(fpDic)>Util.MAX_OPEN:
                #in case we hit the maximum open file limit.
                #close all of them. (reset to zero).
                Util.closeAllFiles(fpDic)
            #Here open the file and store the file descriptor in the fpDic.
            fpDic[city] = open(dir+"/"+city+".txt","a")
        print(line,file=fpDic[city]) #write the line of text to the file.
        
class Entry:
# each line contains a sales record.
# Tab separated fields-
# Date, Time, City , Item Category, sales value, Payment type 
    def __init__(self,line=""):
        self.line=""
        self.valid = False      # assume the record is invalid
        self.svalue=0           # sales value of the record , init to 0 cent.
    def verify(self,line):
        #Verify if the line string contains a valid sales record
        #A valid record consists of the 6 (tab separated) sales record fields.
        self.line = line # for output purpose.
        cols = line.split('\t') # split the line into a list of 6 columns
        self.valid = False      # assume the record is invalid
        self.svalue=0           # sales value of the record , init to 0 cent.
        if len(cols) == 6:
            try:
                self.city = cols[Util.cityCol].strip()
                self.item = cols[Util.itemCol].strip()
                self.svalue=int(float(cols[Util.salesCol])*100)
                # svalue constains the sales amount in cents.
                if self.svalue >=0: # 0 cent is the minimum figure. 0 for free gift.
                    self.valid = True  # reach here implies this is a valid record.
                if len(self.city) == 0 or len(self.item) == 0:
                    self.valid = False # cannot have empty city nor item
            except Exception as e:
                #reach here implies invalid sales amount.
                #self.valid should remain as False
                pass
    def sample(): # a static method - for debugging only
        a='Date\tTime\tCity\tCategory\t12.01\tCash'
        return a
class SalesData:
    # Sales Data object can be used to store
    # either a sales summary of a city
    # or a sales summary of a item category.
  
    def __init__(self,name,e):
        self.name = name # either a city name or a category name
        self.sum = 0     # Total sum of sales of a city or a category (in cents)
                 
    def addEntry(self,e):
        #This adds the entry sales amount of e to the total sum of the
        #sales summary.
         if e.valid:
            # add the sales value to self.sum
            self.sum += e.svalue

    def getSum(self):
        # just return the total sum of sales
        return self.sum

