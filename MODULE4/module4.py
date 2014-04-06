'''
module4.py

Project: United States Trip File Generation
Author: A.P. Hill Wyrough
version date: 3/15/2014
Python 3.3

PURPOSE: Assign Each Resident an Activity Pattern
INPUTS: Activity Pattern Distributions
DEPENDENCIES: None
'''


import csv
from datetime import datetime
import random
import bisect
'----------PATH DEFINITIONS---------------------'
rootDrive = 'E'
rootFilePath = rootDrive + ':\\Thesis\\Output\\'
inputFileNameSuffix = 'Module3NN3rdRun.csv'
outputFileNameSuffix = 'Module4NN2ndRun.csv'

dataDrive = 'E'
dataRoot = dataDrive + ':\\Thesis\\Data\\'
'-----------------------------------------------'
def readActivityPatternDistributions():
    fileLocation = dataRoot + '\\Trip Distributions and Times\\' + 'TripTypeDistributions.csv'
    f = open(fileLocation, 'r+')
    zero = []; one = []; two = []; three = []; four = []; five = []; six = []
    allDistributions = [zero, one, two, three, four, five, six]
    for row in f:
        splitter = row.split(',')
        count = 0
        for j in splitter:
            allDistributions[count].append(float(j.strip('\n'))); count+=1
    f.close()
    return(allDistributions)

'Create Cumulative Distribution'
def cdf(weights):
    total=sum(weights); result=[]; cumsum=0
    for w in weights:
        cumsum+=w
        result.append(cumsum/total)
    return result
            
def assignActivityPattern(travelerType, allDistributions, person):
    'Revise Traveler Type, In the event of no school assigned (incredibly fringe population < 0.001%)'
    if person[len(person) - 3] == 'NA' and (travelerType == 3 or travelerType == 4 or travelerType == 2 or travelerType == 1):
        travelerType = 6
    dist = allDistributions[travelerType]
    weights = cdf(dist)
    split = random.random()
    idx = bisect.bisect(weights, split)
    return idx

'WRITE MODULE 2 OUTPUT HEADERS'
def writeHeaders(pW):
    pW.writerow(['Residence State'] + ['County Code'] + ['Tract Code'] + ['Block Code'] + ['HH ID'] + ['HH TYPE'] + ['Latitude'] + ['Longitude'] 
                + ['Person ID Number'] + ['Age'] + ['Sex'] + ['Traveler Type'] + ['Income Bracket']
                + ['Income Amount'] + ['Work County'] + ['Work Industry'] + ['Employer'] + ['Work Address'] + ['Work City'] + ['Work State'] 
                + ['Work Zip'] + ['Work County Name'] + ['NAISC Code'] + ['NAISC Description'] + ['Patron:Employee'] + ['Patrons'] + ['Employees'] + ['Work Lat'] + ['Work Lon'] 
                + ['School Name'] + ['School County'] + ['SchoolLat'] + ['SchoolLon'] + ['Activity Pattern'])

def executive(state):
    'Module 3 Input Path'
    fileLocation = rootFilePath + 'Module 3\\Third Runs\\' + state + inputFileNameSuffix
    'Module 4 Output Path'
    outputLocation = rootFilePath + 'Module 4\\' + state + outputFileNameSuffix
    'Begin Reporting'
    startTime = datetime.now()
    print(state + " started at: " + str(startTime))
    
    'Open State File'
    f = open(fileLocation, 'r')
    personReader = csv.reader(f, delimiter=',')
    out = open(outputLocation, 'w+', encoding='utf8')
    personWriter = csv.writer(out, delimiter=',', lineterminator='\n')
    writeHeaders(personWriter)
    count = -1
    'Read Distributions'
    distributions = readActivityPatternDistributions()
    'Assign Every Resident a Tour Type AND Write Start of Trip File'
    for person in personReader:
        if count == -1: count+=1; continue
        'Assign Activity Pattern from Revised Traveler Type'
        travelerType = int(person[11])
        if travelerType == 5 and person[14] == '-2':
            activityIndex = '-5'
        else:
            activityIndex = assignActivityPattern(travelerType, distributions, person)
        personWriter.writerow(person + [activityIndex])
        count += 1
        if count % 100000 == 0:
            print(str(count) + ' Residents Completed')
    f.close()
    out.close()  
    print(str(count) + ' of all Residents in ' + state + ' have been processed')
    print(state + " took this much time: " + str(datetime.now()-startTime))
      
import sys
exec('executive(sys.argv[1])')   
        
