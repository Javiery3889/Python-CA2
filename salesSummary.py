#!/usr/bin/env python3

# Phase 1 of Python assignment 
# This application is simulating a sales report generator for a departmental stores in United States of America. 
# Author: Javier Yong 1726682 DISM/1A/21
# Estimated runtime: 1-2mins depending on computer's processing power

import os #for file I/O operations
import sys #for reading user input from command line
import shutil
import myfunctions #import all function from subfunctions created in mymethods.py

# main function
if len(sys.argv) != 2: #checks if the command line has less or more than two arugments
    print("Usage: salesSummary.py <sales data text file>")
else:
    filename = sys.argv[1] #initialise filename variable to store file path for purchases.txt 
    try:
        f = open(filename) 
    except FileNotFoundError: #catch error if file does not exist
        print("Invalid data file. Operation aborted.")
    else:
        myfunctions.gettime() #display current time at start of program if file exists
        currentwd = os.getcwd() 
        path = currentwd + "/reports" #initialise path variable store the string of the reports directory from the current working directory
        if os.path.isdir(path) is True: #check if /reports directory exits
            shutil.rmtree(path) #remove /reports directory and all files and subdirectories in it
        
        #else create /reports directory
        os.mkdir(path) 

        citysalesdict, itemsalesdict = myfunctions.updatedict(f,path) 
        #declare two variables, citysalesdict and itemsalesdict, to store the dictionary containing city:salesvalue pairs and 
        #another dictionary containing itemcategory:salesvalue pairs that is returned from myfunctions.updatedict

        #we can calculate the total sales by using sum function by summing all the values in the dictionary
        totalsales = sum(citysalesdict.values())        
        
        #we also can calculate the average sales for cities and item categories by using len function to find number of key:value
        # pair in each dictionary    
        cityavg = totalsales/len(citysalesdict)
        itemavg = totalsales/len(itemsalesdict)


        #afterwards we sort both dictionaries by salesvalue as it will be easier to access to top and bottom three cities and 
        #item categories later on while printing, this is done using the sorted method which returns an
        # ascending order of list of tuples from the dictionary
        sorted_citysalesdict = myfunctions.sortdict(citysalesdict)
        sorted_itemsalesdict = myfunctions.sortdict(itemsalesdict)
        
        #we can set these two dictionaries to none as we do not need them anymore
        citysalesdict = None 
        itemsalesdict = None
       
        print("Total Sales of the year is {0:8.2f}\n".format(totalsales)) 
        print("The Average Sales From\t{0} Cities :\n{1:44.2f}\n".format(len(sorted_citysalesdict),cityavg))
        
        if len(sorted_citysalesdict) <= 3: #check if there are more than three cities in the sorted_citysalesdict (a list of tuples)
            print("Sales Figures by Cities")
            myfunctions.printdefault(sorted_citysalesdict) #print city and its respective sales value for sales records for that have less than or equals to three cities

        else:
            print("Top Three Cities") 
            myfunctions.printtopthree(sorted_citysalesdict) #else print top 3 cities and their respective sales value for sales records for that have more than three cities
            print("Bottom Three Cities")
            myfunctions.printbottomthree(sorted_citysalesdict) #and print bottom three cities and thier respective sales value for sales records

        print("The Average Sales From\t{0} Item Categories:\n{1:44.2f}\n".format(len(sorted_itemsalesdict),itemavg))
        
        if len(sorted_itemsalesdict) <= 3: #check if there are more than three item categories in sorted_itemsalesdict
            print("Sales Figures by Item Categories")
            myfunctions.printdefault(sorted_itemsalesdict) #print item categories and its respective sales value for sales records for that have less than or equals to three item categories
        else:
            print("Top Three Item Categories")
            myfunctions.printtopthree(sorted_itemsalesdict) #else print top 3 item categories and their respective sales value for sales records for that have more than three categories
            print("Bottom Three Item Categories")
            myfunctions.printbottomthree(sorted_itemsalesdict)  
        myfunctions.gettime() #display current time on machine when program ends

'''
References:
Removing trailing zeros in strftime - https://stackoverflow.com/questions/904928/python-strftime-date-without-leading-0
strftime method - https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
Updating dictionaries efficiently - https://stackoverflow.com/questions/15456158/python-dict-update-vs-subscript-to-add-a-single-key-value-pair
range method - https://www.pythoncentral.io/pythons-range-function-explained/
'''
        

        
