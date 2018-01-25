#!/usr/bin/env python3
import datetime
import sys
import os

# gettime function used to get and print current time displayed on user's machine using the various methods in datetime module
def gettime():
    curtime = datetime.datetime.now() #Return the current local date and time.
    print(curtime.strftime("%a %b %u  %-d %H:%M:%S")) #formats date and time to the same format as assignment using strftime method

#printdivider takes in the integer variable of len which is multiplied with the "=" character and prints the resulant string, this function is used to separate print statements
def printdivider(len=45):
    print("="*len)

# printdefault takes in the input parameter of a list of tuples after a dictionary has been sorted, hence the input parameter is called
# sorted_dict. This function will traverse the list of tuples in reversed order, printing the city or item category
# with the highest sales value, along with its respective sales value. This function is only used for files that contain less than or eqauls to
# 3 cities or 3 item categories

def printdefault(sorted_dict):
    printdivider()
    for i in range(len(sorted_dict)-1,-1,-1): #reversed method reverses the iterator of range, the iterator instead starts from the last element and ends at the first element 
        print("{0:22}{1:>23.2f}".format(sorted_dict[i][0],sorted_dict[i][1]))
    printdivider()
    print()

# printtopthree function takes in the input parameter of a list of tuples after a dictionary has been sorted.
# This function will traverse the list of tuples from the last element to the third last element, printing out
# the top three cities or item categories that has the top 3 highest sales values 
def printtopthree(sorted_dict):
    printdivider()
    for i in range(len(sorted_dict)-1,len(sorted_dict)-4,-1):
        print("{0:22}{1:>23.2f}".format(sorted_dict[i][0],sorted_dict[i][1]))
    printdivider()
    print()

# printbottomthree function takes in the input parameter of a list of tuples after a dictionary has been sorted.
# This function will traverse the list of tuples from the third element to the first element, printing out
# the bottom three cities or item categories that has the bottom three sales values 
def printbottomthree(sorted_dict):
    printdivider()
    for i in range(2,-1,-1):
        print("{0:22}{1:>23.2f}".format(sorted_dict[i][0],sorted_dict[i][1]))
    printdivider()
    print()

#updatedict takes in a file pointer variable (f), and path being the path of the reports directory. the function first intialises three dictionaries. Afterwards,
#the function reads each line of input file using a for loop. It will then write each line to its respective file and update the respective dictionary. This
#function returns two dictionaires citysalesdict and itemsalesdict.
def updatedict(f,path):
    citysalesdict = {} #initialise two variables that will store city:salesvalue pair and itemcategory:salesvalue pair respectively
    itemsalesdict = {}
    cityfiledict = {} #used in when storing file pointers of the files created in reports directory as the value, the key will be the city name.
    for line in f: #for loop to read each line in sales records file
        splitline = line.split("\t")
        filepath = os.path.join(path,splitline[2]) #initialise filepath variable to store filepath with the file name of the city read in the current line in reports directory

        if splitline[2] not in cityfiledict.keys(): #check if key (city) in cityfiledict
            cityfiledict[splitline[2]] = open(filepath + ".txt","a") #store file pointer to each city as the value of cityfiledict

        cityfiledict[splitline[2]].write(line) #write the respective lines to the respective city-named files

        try: #try statement executed when key (city) is found in dictionary
            currentvalue = float(citysalesdict[splitline[2]])
            sumof = currentvalue + float(splitline[4])
            citysalesdict[splitline[2]] = sumof
        except KeyError: #except statemenet is executed when key is not found in citysalesdict
            citysalesdict[splitline[2]]=float(splitline[4])
 
        try: #try statement executed when key (item category) is found in itemsalesdict
            currentvalue = float(itemsalesdict[splitline[3]])
            sumof = currentvalue + float(splitline[4])
            itemsalesdict[splitline[3]] = sumof
        except KeyError: #except statemenet is executed when key is not found in itemsalesdict
            itemsalesdict[splitline[3]]=float(splitline[4])
             
    f.close()
    return citysalesdict,itemsalesdict

#sortdict takes in a dictionary variable (citysalesdict or itemsalesdict), and sorts the dictionary based on the value of the key:value pair (in this case is
# the sales value of the corresponding city or item categories. This is done using the sorted method which returns a list of tuples, each tuple contains the 
#key:value pair from the dictionary. This list of tuples is stored in sorted_dict and is returned
def sortdict(dictionary):
    sorted_dict = sorted(dictionary.items(),key = lambda x: x[1]) # using key argument with a lambda function.
    return sorted_dict
#Note. x represent the individual record (city:salesvalue or itemcategory:salesvalue). x[1] refers to the salesvalue column.

