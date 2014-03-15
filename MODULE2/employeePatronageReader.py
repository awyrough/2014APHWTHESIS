'READ IN EMPLOYEE PATRONAGE FILE FOR A GIVEN COUNTY/STATE, GENERATE DISTRIBUTIONS OF WEIGHTED '
'EMPLOYEE ATTRACTIONS'

from datetime import datetime
import csv
import countyAdjacencyReader
import numpy as np

'MAIN PATH ON MY COMPUTER TOWARDS MODULE1 OUTPUT'
O_PATH = "C:\\Users\\Hill\\Desktop\\Thesis\\Data\\Output\\Module1\\Second Run Complete\\"
M_PATH = "C:\\Users\\Hill\\Desktop\\Thesis\\Data\\"

'Global Variable for Journey to Work Complete Census Data'
j2w = []
   
'RETURN THE WORK COUNTY GIVEN RESIDENT, GENDER, AGE, HOUSEHOLD TYPE, and TRAVELER TYPE.'
def get_work_county(homefips, hht, tt):
    global j2wDist
    if tt in [0,1,3,6] or hht in [2, 3, 4, 5, 7]:
        return -1
    elif tt in [2,4]:
        return homefips
    else:
        return countyFlowDist.select()[1:]

'READ IN ASSOCIATED STATE ABBREVIATIONS WITH STATE FIPS CODES'
def read_states():
    stateFileLocation = M_PATH + '\\'
    fname = stateFileLocation + 'ListofStates.csv'
    lines = open(fname).read().splitlines()
    return lines

'EXECUTIVE FUNCTION TO ASSIGN WORKERS TO A WORK COUNTY, WORK INDUSTRY, AND WORK PLACE'
def executive(state):
    global j2w
    global countyFlowDist
    j2w = countyAdjacencyReader.read_J2W()
    startTime = datetime.now()
    print(state + " started at: " + str(startTime))
    
    'OPEN STATE RESIDENCY FILE'
    fname = O_PATH + state + 'Module1NN2ndRun.csv'
    f = open(fname, 'r')
    personReader = csv.reader(f , delimiter= ',')
    'ITERATE OVER ALL RESIDENTS WITHIN STATE'
    count = 0; trailingFIPS = ''
    for row in personReader:
        'Skip First Row'
        if count == 0:
            count += 1
            continue
        'ASSIGN WORK COUNTY--------------------------------------------------------------------------------------------------------------'
        'Get County Fips Code'
        fips = row[0]+row[1]
        #print(row)
        #print(fips)
        'Track County Code Through State File'
        if (fips != trailingFIPS):
            trailingFIPS = fips
            print(trailingFIPS)
            'Initialize New County J2W Distribution'
            array = countyAdjacencyReader.get_movements(trailingFIPS, j2w)
            countyFlowDist = countyAdjacencyReader.j2wDist(array)
            it, vals = countyFlowDist.get_items()
        'If Distribution is Exhausted, Rebuild From Scratch (not ideal, but assumptions were made to distribution of TT that are not right'
        'FAIL SAFE: DOES NOT HAPPEN AT ALL OFTEN'
        if (countyFlowDist.total_workers() == 0):
            array = countyAdjacencyReader.get_movements(trailingFIPS, j2w)
            countyFlowDist = countyAdjacencyReader.j2wDist(array)
            it, vals = countyFlowDist.get_items()
        'Get Gender, Age, HHT, TT'
        gender = int(row[10]); age = int(row[9]); hht = int(row[5]); tt = int(row[11])
        workCounty = get_work_county(fips, hht, tt)
        #print(workCounty)
        'ASSIGN WORK INDUSTRY------------------------------------------------------------------------------------------------------------'
        'ASSIGN WORK PLACE---------------------------------------------------------------------------------------------------------------'
    
    print(state + " took this much time: " + str(datetime.now()-startTime))
        

#TESTING
#executive('DC')
