'''
module2.py

Project: United States Trip File Generation - Module 2
Author: A.P. Hill Wyrough
version date: 3/15/2014
Python 3.3

Purpose: This is the executive function for Task 2 (Module 2) that assigns a work place to every 
eligible worker. It reads in a state residence file and iterates over every resident.

Dependencies: None

Notes: The structure is inspired by Mufti's Module 2, and get_work_county() helper function is an 
updated version of his. 

''' 
from datetime import datetime
import csv
import countyAdjacencyReader
import industryReader
import workPlaceHelper
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
        val = countyFlowDist.select()
        if (val[0] != '0'):
            return -2
        if (int(val[1]) > 5):
            return -2
        else:
            return val[1:]
'READ IN ASSOCIATED STATE ABBREVIATIONS WITH STATE FIPS CODES'
def read_states():
    stateFileLocation = M_PATH + '\\'
    fname = stateFileLocation + 'ListofStates.csv'
    lines = open(fname).read().splitlines()
    return lines
'WRITE MODULE 2 OUTPUT HEADERS'
def writeHeaders(pW):
    pW.writerow(['Residence State'] + ['County Code'] + ['Tract Code'] + ['Block Code'] 
                  + ['HH ID'] + ['HH TYPE'] + ['Latitude'] + ['Longitude'] 
                  + ['Person ID Number'] + ['Age'] + ['Sex'] + ['Traveler Type'] 
                  + ['Income Bracket'] + ['Income Amount'] + ['Work County'] + ['Work Industry'] 
                  + ['Employer'] + ['Work Address'] + ['Work City'] + ['Work State'] 
                  + ['Work Zip'] + ['Work County Name'] + ['NAISC Code'] + ['NAISC Description'] 
                  + ['Patron:Employee'] + ['Patrons'] + ['Employees'] + ['Work Lat'] + ['Work Lon'] )
'---------------------------------------------------------------------------------------------------'
'EXECUTIVE FUNCTION TO ASSIGN WORKERS TO A WORK COUNTY, WORK INDUSTRY, AND WORK PLACE'
def executive(state):
    global j2w
    global countyFlowDist
    outputPath = "C:\\Users\\Hill\\Desktop\\Thesis\\Data\\Output\\Module2\\"
    'Read In J2W and Employment by Income by Industry'
    j2w = countyAdjacencyReader.read_J2W()
    menemp, womemp, meninco, wominco = industryReader.read_employment_income_by_industry()   
    'Begin Progress Reporting Initialization'
    startTime = datetime.now()
    print(state + " started at: " + str(startTime))
    'OPEN STATE RESIDENCY FILE'
    fname = O_PATH + state + 'Module1NN2ndRun.csv'
    f = open(fname, 'r')
    personReader = csv.reader(f , delimiter= ',')
    out = open(outputPath + str(state + 'Module2NN1stRun.csv'), 'w+', encoding='utf8')
    personWriter = csv.writer(out, delimiter=',', lineterminator='\n')
    writeHeaders(personWriter)
    ############ RUN ###################
    'ITERATE OVER ALL RESIDENTS WITHIN STATE'
    count = 0; trailingFIPS = ''
    workingCounties = []
    workingCountyObjects = []
    for row in personReader:
        'Skip First Row'
        if count == 0:
            count += 1
            continue
        'ASSIGN WORK COUNTY----------------------------------------------------------------'
        'Get County Fips Code'
        fips = row[0]+row[1]
        if len(fips) != 5:
            fips = '0' + fips
        'Track County Code Through State File'
        if (fips != trailingFIPS):
            trailingFIPS = fips
            'Reset Home County'
            workingCounties = []
            workingCountyObjects = []
            'Initialize New County J2W Distribution'
            array = countyAdjacencyReader.get_movements(trailingFIPS, j2w)
            countyFlowDist = countyAdjacencyReader.j2wDist(array)
            it, vals = countyFlowDist.get_items()
        'If Distribution is Exhausted, Rebuild From Scratch (not ideal, but'
        'assumptions were made to distribution of TT that are not right'
        'FAIL SAFE: SHOULD NOT HAPPEN'
        if (countyFlowDist.total_workers() == 0):
            array = countyAdjacencyReader.get_movements(trailingFIPS, j2w)
            countyFlowDist = countyAdjacencyReader.j2wDist(array)
            it, vals = countyFlowDist.get_items()
        'Get Gender, Age, HHT, TT, Income, HomeLat, HomeLon'
        gender = int(row[10]); age = int(row[9]); hht = int(row[5]); 
        tt = int(row[11]); income = float(row[13]); lat = float(row[7]); lon = float(row[8])
        workCounty = get_work_county(fips, hht, tt)
        'ASSIGN WORK INDUSTRY AND WORK PLACE-------------------------------------------------'
        if (workCounty != -1) and (workCounty != -2):
            'Check If WorkCounty Has Not Already Been Initialized, if not, Add it'
            if workCounty not in workingCounties:
                workingCounties.append(workCounty)
                newWorkCounty = workPlaceHelper.workingCounty(workCounty)
                workingCountyObjects.append([workCounty, newWorkCounty])
            'Select Employer'
            for j in workingCountyObjects:
                if j[0] == workCounty:
                    workIndustry, index, employer = j[1].select_industry_and_employer(lat, lon, str(workCounty), 
                                                               gender, income, menemp, womemp, meninco, wominco)
                    break    
        else:
            if (workCounty == -1): 
                workIndustry = '-1'
                employer = ['Non-Worker'] + ['NA']+['NA']+['NA']+['NA']+['NA']+['NA']
                        +['NA']+['NA']+['NA']+['NA']+['NA']+['NA']+['NA']+['NA']+['NA']+['NA']
            else: 
                workIndustry = '-2'
                employer = ['International Destination for Work'] + ['NA']+['NA']+['NA']+['NA']
                +['NA']+['NA']+['NA']+['NA']+['NA']+['NA']+['NA']+['NA']+['NA']+['NA']+['NA']+['NA']

        personWriter.writerow(row + [workCounty] + [workIndustry] + [employer[0]] + [employer[1]] 
                                 + [employer[2]] + [employer[3]] + [employer[4]] + [employer[5]] 
                                 + [employer[9]] + [employer[10]] + [employer[11]] + [employer[12]] 
                                 + [employer[13]] + [employer[15]] + [employer[16]])
        'PROGRESS REPORTING-------------------------------------------------------------------------'    
        count+=1
        if count % 10000 == 0:
            print(str(count) + ' residents done')
            print('Time Elapsed: ' + str(datetime.now() - startTime))
        if count % 50000 == 0:
            print('Time Elapsed: ' + str(datetime.now() - startTime))
    print(str(count) + ' residents done')    
    print(state + " took this much time: " + str(datetime.now()-startTime))

import sys
import cProfile
cProfile.run("executive(sys.argv[1])")
