import csv
import activityPattern
import findOtherTrips
import classDumpModule5
from datetime import datetime

'iterate through activity pattern object, finding other trips based off of previous node'

'need someway to trim down patronage data - read file, throw out non zero patronage'
'select industry based off purpose?'

'----------PATH DEFINITIONS---------------------'
rootDrive = 'E'
rootFilePath = rootDrive + ':\\Thesis\\Output\\'
inputFileNameSuffix = 'Module4NN2ndRun.csv'
outputFileNameSuffix = 'Module5NN1stRun.csv'

dataDrive = 'E'
dataRoot = dataDrive + ':\\Thesis\\Data\\'
'-----------------------------------------------'

'WRITE MODULE 2 OUTPUT HEADERS'
def writeHeaders(pW):
    pW.writerow(['Residence State'] + ['County Code'] + ['Tract Code'] + ['Block Code'] + ['HH ID'] 
                + ['Person ID Number'] + ['Activity Pattern']
                + ['Node 1 Type'] + ['Node 1 Predecessor'] + ['Node 1 Successor'] + ['Node 1 Name'] + ['Node 1 County'] + ['Node 1 Lat'] + ['Node 1 Lon']
                + ['Node 2 Type'] + ['Node 2 Predecessor'] + ['Node 2 Successor'] + ['Node 2 Name'] + ['Node 2 County'] + ['Node 2 Lat'] + ['Node 2 Lon']
                + ['Node 3 Type'] + ['Node 3 Predecessor'] + ['Node 3 Successor'] + ['Node 3 Name'] + ['Node 3 County'] + ['Node 3 Lat'] + ['Node 3 Lon']
                + ['Node 4 Type'] + ['Node 4 Predecessor'] + ['Node 4 Successor'] + ['Node 4 Name'] + ['Node 4 County'] + ['Node 4 Lat'] + ['Node 4 Lon']
                + ['Node 5 Type'] + ['Node 5 Predecessor'] + ['Node 5 Successor'] + ['Node 5 Name'] + ['Node 5 County'] + ['Node 5 Lat'] + ['Node 5 Lon']
                + ['Node 6 Type'] + ['Node 6 Predecessor'] + ['Node 6 Successor'] + ['Node 6 Name'] + ['Node 6 County'] + ['Node 6 Lat'] + ['Node 6 Lon']
                + ['Node 7 Type'] + ['Node 7 Predecessor'] + ['Node 7 Successor'] + ['Node 7 Name'] + ['Node 7 County'] + ['Node 7 Lat'] + ['Node 7 Lon'])

def executive(state):
    'Module 4 Input Path'
    fileLocation = rootFilePath + 'Module 4\\' + state + inputFileNameSuffix
    'Module 5 Output Path'
    outputLocation = rootFilePath + 'Module 5\\'
    'Begin Reporting'
    startTime = datetime.now()
    print(state + " started at: " + str(startTime))
    trailingFIPS = ''
    'Open State File'
    f = open(fileLocation, 'r')
    personReader = csv.reader(f, delimiter=',')
    
    count = -1
    
    homeCountyPatronage = findOtherTrips.patronageWarehouse()
    countyNameData = classDumpModule5.read_counties()
    
    for person in personReader:
        if count == -1: count+=1; continue
        newCounty = person[0] + person[1]
        'Initialize new home county patronage lists'        
        if newCounty != trailingFIPS:
            trailingFIPS = newCounty
            print(trailingFIPS)
            out = open(outputLocation + state + '_' + trailingFIPS + '_' + outputFileNameSuffix, 'w+', encoding='utf8')
            personWriter = csv.writer(out, delimiter=',', lineterminator='\n')
            writeHeaders(personWriter)
            homeCountyPatronage = findOtherTrips.patronageWarehouse()
            homeCountyPatronage.homeCounties.append(findOtherTrips.patronageCounty(newCounty))
        
        'Assemble Daily Tour Object and Populate Existing Trip Information (For Home, School, Work)'
        personalTour = activityPattern.activityPattern(int(person[len(person) - 1]), person)
        'Populate Trip Tour With Other Trips'
        personalTour, homeCountyPatronage = findOtherTrips.populateActivities(personalTour, person, homeCountyPatronage, person[0], countyNameData)
        'Output Trip Tour and Information to County Trip File'
        personWriter.writerow([person[0]] + [person[1]] + [person[2]] + [person[3]] + [person[4]] + [person[8]] + [int(person[len(person) - 1])] +
                              [personalTour.activities[0][0]] + [personalTour.activities[0][2]] + [personalTour.activities[0][3]] + [personalTour.activities[0][4]] + [personalTour.activities[0][5]] + [personalTour.activities[0][6]] + 
                              [personalTour.activities[1][0]] + [personalTour.activities[1][2]] + [personalTour.activities[1][3]] + [personalTour.activities[1][4]] + [personalTour.activities[1][5]] + [personalTour.activities[1][6]] + 
                              [personalTour.activities[2][0]] + [personalTour.activities[2][2]] + [personalTour.activities[2][3]] + [personalTour.activities[2][4]] + [personalTour.activities[2][5]] + [personalTour.activities[2][6]] + 
                              [personalTour.activities[3][0]] + [personalTour.activities[3][2]] + [personalTour.activities[3][3]] + [personalTour.activities[3][4]] + [personalTour.activities[3][5]] + [personalTour.activities[3][6]] + 
                              [personalTour.activities[4][0]] + [personalTour.activities[4][2]] + [personalTour.activities[4][3]] + [personalTour.activities[4][4]] + [personalTour.activities[4][5]] + [personalTour.activities[4][6]] + 
                              [personalTour.activities[5][0]] + [personalTour.activities[5][2]] + [personalTour.activities[5][3]] + [personalTour.activities[5][4]] + [personalTour.activities[5][5]] + [personalTour.activities[5][6]] + 
                              [personalTour.activities[6][0]] + [personalTour.activities[6][2]] + [personalTour.activities[6][3]] + [personalTour.activities[6][4]] + [personalTour.activities[6][5]] + [personalTour.activities[6][6]])
        count += 1
        if count % 50000 == 0:
            print(str(count) + ' Residents Completed and taken this much time: ' + str(datetime.now()-startTime))
    f.close()
    out.close()  
    print(str(count) + ' of all Residents in ' + state + ' have been processed')
    print(state + " took this much time: " + str(datetime.now()-startTime))

import sys
import cProfile
cProfile.run('exec("executive(sys.argv[1])")')
#exec("executive('Montana')")