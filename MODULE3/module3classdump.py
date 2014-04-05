import math
import csv
'----------PATH DEFINITIONS---------------------'
rootDrive = 'E'
rootFilePath = rootDrive + ':\\Thesis\\Output\\'
inputFileNameSuffix = 'Module4NN2ndRun.csv'
outputFileNameSuffix = 'Module5NN1stRun.csv'

dataDrive = 'E'
dataRoot = dataDrive + ':\\Thesis\\Data\\'
'-----------------------------------------------'
def read_states():
    """ Read in State names, abbreviations, and state codes"""
    censusFileLocation = dataRoot
    fname = censusFileLocation + 'ListofStates.csv'
    f = open(fname, 'r+')
    mydata = csv.reader(f, delimiter=',') 
    data = []
    for row in mydata:
        data.append(row)
    return data

def match_abbrev_code(states, abbrev):
    for j in (states):
        #splitter = j.split(',')
        if j[1] == abbrev:
            return j[2]

'Read in County Name to FIPS Code Data'
def read_counties():
    fname = dataRoot + '\\WorkFlow\\allCounties.csv'
    f = open(fname, 'r+')
    namedata = []
    for line in f:
        splitter = line.split(',')
        namedata.append([splitter[3], splitter[6].split(' ')])
    return namedata  

'Match County Name from EMP file to County Name in FIPS Related Data'
def lookup_name(countyname, code, namedata):
    for j in namedata:

        countyname = countyname.strip('"')
        splitter = countyname.split(' ')

        if (splitter[0] == j[1][0]) and (len(splitter) == 1):
            if (j[0][0:2] == code):
                return j[0]
        elif (splitter[0] == j[1][0]) and (splitter[1] == j[1][1]) and (len(splitter)==2):
            if (j[0][0:2] == code):
                return j[0]
        elif (len(j[1]) == 3) and (len(splitter) > 2):
            if (splitter[0] == j[1][0]) and (splitter[1] == j[1][1]) and (splitter[2] == j[1][2]):
                if (j[0][0:2] == code):   
                    return j[0]
        elif (len(j[1]) > 3) and (len(splitter) > 1):
            if (splitter[0] == j[1][0]) and (splitter[1] == j[1][1]):
                if (j[0][0:2] == code):
                    return j[0]
    