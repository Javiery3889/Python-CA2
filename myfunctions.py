import datetime #to get machine's current date and time 
import sys
import os
# gettime function used to get and print current time displayed on user's machine using the various methods in datetime module
def gettime():
    curtime = datetime.datetime.now() #Return the current local date and time.
    print(curtime.strftime("%a %b %u  %-d %H:%M:%S")) #formats date and time to the same format as assignment using strftime method

#printdivider takes in the integer variable of len which is multiplied with the "=" character and prints the resulant string, this function is used to separate print statements
def printdivider(len=44):
    print("="*len)

# printdefault takes in the input parameter of a list of tuples after a dictionary has been sorted, hence the input parameter is called
# sorted_dict. This function will traverse the list of tuples in reversed order, printing the city or item category
# with the highest sales value, along with its respective sales value. This function is only used for files that contain less than or eqauls to
# 3 cities or 3 item categories

def printdefault(sorted_dict):
    printdivider()
    for i in range(len(sorted_dict)-1,-1,-1): #reversed method reverses the iterator of range, the iterator instead starts from the last element and ends at the first element 
        print("{0:22}{1:>22.2f}".format(sorted_dict[i][0],sorted_dict[i][1]))
    printdivider()
    print()

# printtopthree function takes in the input parameter of a list of tuples after a dictionary has been sorted.
# This function will traverse the list of tuples from the last element to the third last element, printing out
# the top three cities or item categories that has the top 3 highest sales values 
def printtopthree(sorted_dict):
    printdivider()
    for i in range(len(sorted_dict)-1,len(sorted_dict)-4,-1):
        print("{0:22}{1:>22.2f}".format(sorted_dict[i][0],sorted_dict[i][1]))
    printdivider()
    print()

# printbottomthree function takes in the input parameter of a list of tuples after a dictionary has been sorted.
# This function will traverse the list of tuples from the third element to the first element, printing out
# the bottom three cities or item categories that has the bottom three sales values 
def printbottomthree(sorted_dict):
    printdivider()
    for i in range(2,-1,-1):
        print("{0:22}{1:>22.2f}".format(sorted_dict[i][0],sorted_dict[i][1]))
    printdivider()
    print()

#writefile takes in the variable line and path, which is each line form the sales record file and path being the path of the reports directory. 
# This line is then broken down into a list using .split() method.
#Afterwards, the program creates a file with the city name by accessing the third element in the list that was created. We then write the corresponding line
# to that file. Afterwards we return the list as it will be use for dictionary creation later in updatedict function.    
def writefile(line,path):
    splitline = line.split("\t")
    if len(splitline) != 6: #check if file is formatted properly
        print("Invalid file format!")
        sys.exit()
    else:
        with open(os.path.join(path,splitline[2]), 'a') as writeto_file: #create and open a file using os.path.join
            writeto_file.write(line)
            writeto_file.close()
    return splitline

#updatedict takes in a file variable (f) and reads each line of the sales summary using a for loop. Afterwards it stores each list returned from line.split()
#in splitline variable. It then checks if the city/item category is in citysalesdict or itemsalesdict respectivly. If it exists in its respective dictionary,
#it will get the sales value of that splitline list (splitline[4]) and will add that value with value found it the dictionary. Else if the city or item 
# category does not exist, it will just add the entry into the dictionary. Afterwards, the function closes the file and returns both dictionaries. 
def updatedict(f,path):
    citysalesdict = {} #initialise two variables that will store city:salesvalue pair and itemcategory:salesvalue pair respectively
    itemsalesdict = {}
    for line in f: #for loop to read each line in sales records file
        splitline = writefile(line,path) #call writefile function which will write each line to its respective output city file, and store 
        #each list returned from writefile function after using .split() method 
        
        if str(splitline[2]) in citysalesdict:
            currentvalue = float(citysalesdict[str(splitline[2])])
            citysalesdict.update({str(splitline[2]):currentvalue + float(splitline[4])})
        else:
            citysalesdict.update({str(splitline[2]):float(splitline[4])})

        if str(splitline[3]) in itemsalesdict:
            currentvalue = float(itemsalesdict[str(splitline[3])])
            itemsalesdict.update({str(splitline[3]):currentvalue + float(splitline[4])})
        else:
            itemsalesdict.update({str(splitline[3]):float(splitline[4])})
            
    f.close()
    return citysalesdict,itemsalesdict

#sortdict takes in a dictionary variable (citysalesdict or itemsalesdict), and sorts the dictionary based on the value of the key:value pair (in this case is
# the sales value of the corresponding city or item categories. This is done using the sorted method which returns a list of tuples, each tuple contains the 
#key:value pair from the dictionary. This list of tuples is stored in sorted_dict and is returned
def sortdict(dictionary):
    sorted_dict = sorted(dictionary.items(),key = lambda x: x[1]) # using key argument with a lambda function.
    return sorted_dict
#Note. x represent the individual record (city:salesvalue or itemcategory:salesvalue). x[1] refers to the salesvalue column.

