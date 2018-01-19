#!/usr/bin/python3
import os 
import sys 
import datetime
import operator
import shutil

def gettime():
    curtime = datetime.datetime.now()
    print(curtime.strftime("%a %b %u  %-d %H:%M:%S"))

def printdefault(sorted_dict):
    for i in reversed(range(len(sorted_dict))):
        print("{0:22}{1:>22.2f}".format(sorted_dict[i][0],sorted_dict[i][1]))

def printtopthree(sorted_dict):
    for i in range(len(sorted_dict)-1,len(sorted_dict)-4,-1):
        print("{0:22}{1:>22.2f}".format(sorted_dict[i][0],sorted_dict[i][1]))

def printbottomthree(sorted_dict):
    for i in range(2,-1,-1):
        print("{0:22}{1:>22.2f}".format(sorted_dict[i][0],sorted_dict[i][1]))


if len(sys.argv) != 2:
    print("Usage: salesSummary.py <sales data text file>")
else:
    filename = sys.argv[1]    
    try:
        f = open(filename)
    except FileNotFoundError: 
        print("Invalid data file. Operation aborted.")
    else:
        gettime()
        currentwd = os.getcwd()
        path = currentwd + "/reports"
        if os.path.isdir(path) is True:
            shutil.rmtree(path)
        
        os.mkdir(path)
        citysalesdict = {}
        itemsalesdict = {}

        for line in f:
            splitline = line.split("\t")
            line = "\t".join(splitline)
            with open("reports/"+splitline[2], 'a') as writeto_file:
                writeto_file.write(line)
                writeto_file.close()
        
            if str(splitline[2]) in citysalesdict:
                currentvalue = float(citysalesdict[str(splitline[2])])
                sumof = currentvalue + float(splitline[4])
                citysalesdict.update({str(splitline[2]):sumof})
            else:
                citysalesdict.update({str(splitline[2]):float(splitline[4])})

            if str(splitline[3]) in itemsalesdict:
                currentvalue = float(itemsalesdict[str(splitline[3])])
                sumof = currentvalue + float(splitline[4])
                itemsalesdict.update({str(splitline[3]):sumof})
            else:
                itemsalesdict.update({str(splitline[3]):float(splitline[4])})

        f.close()
        sorted_itemsalesdict = sorted(itemsalesdict.items(),key=operator.itemgetter(1))
                    
        totalcitysum = sum(citysalesdict.values())
        cityavg = totalcitysum/len(citysalesdict)

        totalitemsum = sum(itemsalesdict.values())
        itemavg = totalitemsum/len(itemsalesdict)

        sorted_citysalesdict = sorted(citysalesdict.items(), key=operator.itemgetter(1))
        citysalesdict = None 
        itemsalesdict = None
       
        print("Total Sales of the year is\t{0:.2f}".format(totalcitysum))
        print("The Average Sales From\t{0} Cities:\n\t{1:35.2f}".format(len(sorted_citysalesdict),cityavg))
        if len(sorted_citysalesdict) <= 3:
            print("Sales Figures by Cities")
            print("============================================")
            printdefault(sorted_citysalesdict)
            print("============================================")
            print()

        else:
            print("Top Three Cities")
            print("============================================")
            printtopthree(sorted_citysalesdict)
            print("============================================")
            print()
            print("Bottom Three Cities")
            print("============================================")
            printbottomthree(sorted_citysalesdict) 
            print("============================================")
            print()

        print("The Average Sales From\t{0} Item Categories:\n\t{1:35.2f}".format(len(sorted_itemsalesdict),totalitemsum/len(sorted_itemsalesdict)))
        
        if len(sorted_itemsalesdict) <= 3:
            print("Sales Figures by Item Categories")
            print("============================================")
            printdefault(sorted_citysalesdict)
            print("============================================")
            print()    
        else:
            print("Top Three Item Categories")
            print("============================================")
            printtopthree(sorted_itemsalesdict)
            print("============================================")
            print()
            print("Bottom Three Item Categories")
            print("============================================")
            printbottomthree(sorted_itemsalesdict)  
            print("============================================")
            print()
        gettime()
        

        