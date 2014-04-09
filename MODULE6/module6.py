'''
module6.py

Project: United States Trip File Generation - Module 6
Author: A.P. Hill Wyrough
version date: 3/15/2014
Python 3.3

Purpose: This program assigns all daily activity patterns their temporal attributes. It reads in old module 5 trip sequence files
and creates a new one with time attributes.

Dependencies: None

Notes: This is done entirely differently than mufti's - it is adapted to more activity patterns and it uses exponential distributions
not triangular distributions as his did. 
'''
'----------PATH DEFINITIONS---------------------'
rootDrive = 'G'
rootFilePath = rootDrive + ':\\Thesis\\Output\\'
inputFileNameSuffix = 'Module5NN1stRun.csv'
outputFileNameSuffix = 'Module6NN1stRun.csv'

dataDrive = 'G'
dataRoot = dataDrive + ':\\Thesis\\Data\\'
'-----------------------------------------------'
import csv
import random
import math
from datetime import datetime
from os import listdir
from os.path import isfile, join

'ARRIVAL TIME PARAMETERS'
arrivalParameter = 5.0
departureParameter = 5.0
variance = 0.25
speedParameter = 30.0

'CONVERT MODULE 5 INPUT INTO MODULE 6 OBJECTS WITH TIME ADDED'
"['Type', 'Pred', 'Succ', 'Name', 'County', 'Lat', 'Lon', 'Industry', 'oTime', 'dTime']"
def initialize_new_activityPattern(activityPattern):
    pattern = []
    c = 0
    for j in range(0, 7):
        activity = []
        for k in range(0, 8):
            activity.append(activityPattern[c])
            c+=1
        activity.append('oTime')
        activity.append('dTime')
        pattern.append(activity)
    return pattern

'WALK THROUGH TRIP SEQUENCE AND BUILD DAILY SCHEDULE'
'ACCEPTS OLD PERSONAL ACTIVITY PATTERN THEN RETURNS NEW ONE WITH TIME'
def scheduleDay(personalActivity, data, pattern):
    'HANDLE FIRST TRIP'
    home = personalActivity[0]
    home[8] = 0.0
    if home[2] == 'N':
        return personalActivity
    if home[2] == 'W':
        work = personalActivity[1]
        start, end, duration = get_employee_start_end_duration((work[7]), data) 
        dTimeFirst = get_arrival_time(start)
        oTimeFirst = work_backwards(dTimeFirst, home[5], home[6], work[5], work[6])
        workDepartureTime = get_departure_time(end)
        home[9] = oTimeFirst
        work[8] = dTimeFirst
        personalActivity[1][9] = workDepartureTime
        personalActivity[2][8] = work_forwards(workDepartureTime, work[5], work[6], home[5], home[6])
    elif personalActivity[1][0] == 'S':
        school = personalActivity[1]
        dTimeFirst = get_arrival_time(8.5)
        oTimeFirst = work_backwards(dTimeFirst, home[5], home[6], school[5], school[6])
        schoolDepartureTime = get_departure_time(15.5)
        home[9] = oTimeFirst
        school[8] = dTimeFirst
        personalActivity[1][9] = schoolDepartureTime
        personalActivity[2][8] = work_forwards(schoolDepartureTime, personalActivity[1][5], personalActivity[1][6], home[5], home[6])
    elif personalActivity[1][0] == 'O':
        oTimeFirst = random.uniform(10, 12) * 3600
        dTimeFirst = work_forwards(oTimeFirst, home[5], home[6], personalActivity[1][5], personalActivity[1][6])
        duration = get_patronage_duration((personalActivity[1][7]), data) 
        firstPatronage = getDurationTime(duration)
        home[9] = oTimeFirst
        personalActivity[1][8] = dTimeFirst
        personalActivity[1][9] = dTimeFirst + firstPatronage
        personalActivity[2][8] = work_forwards(personalActivity[1][9], personalActivity[1][5], personalActivity[1][6], personalActivity[2][5], personalActivity[2][6])
        if personalActivity[2][2] == 'N':
            return personalActivity
        if personalActivity[2][2] == 'O' and personalActivity[2][0] == 'H':
            personalActivity[2][9] = personalActivity[2][8] + random.uniform(0, 0.50) * 3600
            personalActivity[3][8] = work_forwards(personalActivity[2][9], personalActivity[2][5], personalActivity[2][6], personalActivity[3][5], personalActivity[3][6])
            personalActivity[3][9] = personalActivity[3][8] + getDurationTime(get_patronage_duration((personalActivity[3][7]), data))
            personalActivity[4][8] = work_forwards(personalActivity[3][9], personalActivity[3][5], personalActivity[3][6], personalActivity[4][5], personalActivity[4][6])
            
    'MANAGE LUNCH BREAK TRIPS (HWOW)'
    if pattern == '14':
        personalActivity[3][9] = workDepartureTime
        personalActivity[1][9] = random.uniform(9, 12) * 3600
        personalActivity[2][8] = work_forwards(personalActivity[1][9], personalActivity[1][5], personalActivity[1][6], personalActivity[2][5], personalActivity[2][6])
        duration = get_patronage_duration((personalActivity[2][7]), data)
        patronageTime = getDurationTime(duration)
        personalActivity[2][9] = personalActivity[2][8] + patronageTime
        personalActivity[3][8] = work_forwards(personalActivity[2][9], personalActivity[2][5], personalActivity[2][5], personalActivity[3][5], personalActivity[3][6])
        personalActivity[4][8] = work_forwards(personalActivity[3][9], personalActivity[3][5], personalActivity[3][6], personalActivity[4][5], personalActivity[4][6])
        return personalActivity
    'WALK THROUGH REMAINING TRIPS AND ASSIGN DURATION, ARRIVAL TIME'
    count = 2
    for j in personalActivity[2:]:
        now = j
        current = j[0]
        nextNode = now[2]
        if current == 'H':
            duration = random.uniform(0, 0.30) * 3600.0
        elif current == 'O':
            duration = getDurationTime(get_patronage_duration((now[7]), data))
        elif current == 'S':
            duration = getDurationTime(get_patronage_duration(61, data))
        elif current == 'W':
            duration = random.gauss(4.00, 0.15*4.00) * 3600.0
        if nextNode == 'N':
            now[9] = 'NA'
            break
        now[9] = now[8] + duration
        if count == 6:
            break
        next = personalActivity[count + 1]
        next[8] = work_forwards(now[9], now[5], now[6], next[5], next[6]) 
        count+=1
    return personalActivity

'GET PATRONAGE DURATION TIME GIVEN EXPECTED DURATION'
def getDurationTime(duration):
    return random.gauss(duration, variance * duration)
'GIVEN FIRST TRIP ARRIVAL TIME, AND POSITION OF HOME AND DESTINATION, RETURN SECONDS FROM MIDNIGHT WHEN YOU LEAVE'
def work_backwards(arrivalTime, lat1, lon1, lat2, lon2):
    distance = distance_between_counties(lat1, lon1, lat2, lon2)
    'TIME = DISTANCE * SPEED (IN SECONDS)'
    tripTime = distance / (speedParameter / (3600.0))
    actualArrivalTime = arrivalTime - tripTime
    return actualArrivalTime
'GIVEN NODE DEPARTURE TIME, CALCULATE ARRIVAL TIME AT NEXT POINT'
def work_forwards(departureTime, lat1, lon1, lat2, lon2):
    distance = distance_between_counties(lat1, lon1, lat2, lon2)
    'TIME = DISTANCE * SPEED (IN SECONDS)'
    tripTime = distance / (speedParameter / (3600.0))
    actualArrivalTime = departureTime + tripTime
    return actualArrivalTime
'RETURN MILES BETWEEN LATITUDE AND LONGITUDE POINTS '
def distance_between_counties(lat1, lon1, lat2, lon2):
    degrees_to_radians = math.pi/180.0
    phi1 = (90.0 - float(lat1))*degrees_to_radians
    phi2 = (90.0 - float(lat2))*degrees_to_radians
    theta1 = float(lon1)*degrees_to_radians
    theta2 = float(lon2)*degrees_to_radians
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos(cos)
    return arc * 3963.167
'READ IN SCHEDULE FILES FOR EMP PAT AT NAICS CODES'
def read_schedule_files():
    fileLocation = dataRoot + 'Trip Distributions and Times\\ScheduleFile.csv'
    data = []
    f = open(fileLocation, 'r+')
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        data.append(row)
    return data
'RETURN PATRONAGE DURATION FOR GIVEN NAICS INTEGER CODE'
def get_patronage_duration(naics, data):
    if naics == 'NA' or naics == '99':
        naics = 81
    naics = int(naics)
    if naics in [31, 32, 33]: naics = 31
    if naics in [44, 45]: naics = 44
    if naics in [48, 49]: naics = 48
    for row in data:
        if int(row[1]) == (naics):
            return float(row[5])*3600   
'RETURN EMPLOYEE START BELL, END BELL, DURATION FOR GIVEN NAICS INTEGER CODE'
def get_employee_start_end_duration(naics, data):
    if naics == 'NA' or naics == '99':
        naics = 81
    naics = int(naics)
    if naics in [31, 32, 33]: naics = 31
    if naics in [44, 45]: naics = 44
    if naics in [48, 49]: naics = 48
    for row in data:
        if int(row[1]) == naics:
            return float(row[2]), float(row[3]), float(row[4])
'RETURN ARRIVAL TIME FOR GIVEN START BELL TIME (IN SECONDS FROM MIDNIGHT)'
def get_arrival_time(bellTime):
    'COMPUTE ARRIVAL WINDOW TIME IN MINUTES'
    windowTime = random.expovariate(1.0/arrivalParameter)
    'COMPUTE ACTUAL ARRIVAL TIME IN SECONDS FROM MIDNIGHT'
    secondsInWindow = 60.0 * windowTime
    arrivalTime = bellTime*3600.0 - (10.0*60.0 - secondsInWindow)
    return arrivalTime
'RETURN DEPARTURE TIME FOR GIVEN END BELL TIME (IN SECONDS FROM MIDNIGHT)'
def get_departure_time(bellTime):
    'COMPUTE ARRIVAL WINDOW TIME IN MINUTES'
    windowTime = random.expovariate(1.0/arrivalParameter)
    'COMPUTE ACTUAL ARRIVAL TIME IN SECONDS FROM MIDNIGHT'
    secondsInWindow = 60.0 * windowTime
    departureTime = bellTime*3600.0 + secondsInWindow
    return departureTime 
'WRITE MODULE 6 HEADERS'
def writeHeaders(pW):
        pW.writerow(['Residence State'] + ['County Code'] + ['Tract Code'] + ['Block Code'] + ['HH ID'] + ['Person ID Number'] + ['Activity Pattern']
                + ['Node 1 Type'] + ['Node 1 Predecessor'] + ['Node 1 Successor'] + ['Node 1 Name'] + ['Node 1 County'] + ['Node 1 Lat'] + ['Node 1 Lon'] + ['Node 1 Arrival Time'] + ['Node 1 Departure Time'] 
                + ['Node 2 Type'] + ['Node 2 Predecessor'] + ['Node 2 Successor'] + ['Node 2 Name'] + ['Node 2 County'] + ['Node 2 Lat'] + ['Node 2 Lon'] + ['Node 2 Arrival Time'] + ['Node 2 Departure Time'] 
                + ['Node 3 Type'] + ['Node 3 Predecessor'] + ['Node 3 Successor'] + ['Node 3 Name'] + ['Node 3 County'] + ['Node 3 Lat'] + ['Node 3 Lon'] + ['Node 3 Arrival Time'] + ['Node 3 Departure Time']   
                + ['Node 4 Type'] + ['Node 4 Predecessor'] + ['Node 4 Successor'] + ['Node 4 Name'] + ['Node 4 County'] + ['Node 4 Lat'] + ['Node 4 Lon'] + ['Node 4 Arrival Time'] + ['Node 4 Departure Time']  
                + ['Node 5 Type'] + ['Node 5 Predecessor'] + ['Node 5 Successor'] + ['Node 5 Name'] + ['Node 5 County'] + ['Node 5 Lat'] + ['Node 5 Lon'] + ['Node 5 Arrival Time'] + ['Node 5 Departure Time'] 
                + ['Node 6 Type'] + ['Node 6 Predecessor'] + ['Node 6 Successor'] + ['Node 6 Name'] + ['Node 6 County'] + ['Node 6 Lat'] + ['Node 6 Lon'] + ['Node 6 Arrival Time'] + ['Node 6 Departure Time']  
                + ['Node 7 Type'] + ['Node 7 Predecessor'] + ['Node 7 Successor'] + ['Node 7 Name'] + ['Node 7 County'] + ['Node 7 Lat'] + ['Node 7 Lon'] + ['Node 7 Arrival Time'] + ['Node 7 Departure Time'] )

'READ IN COUNTY FILE AND CREATE NEW COUNTY TRIP FILE WITH TIME ATTRIBUTES'
def executive(filename, state):
    'READ INPUT'
    inputFile = rootFilePath + 'Module 5\\' + state + '\\' + filename
    f = open(inputFile, 'r+')
    reader = csv.reader(f, delimiter=',')
    'CREATE OUTPUT'
    splitter = filename.split('_')
    outputFile = rootFilePath + 'Module 6\\' + state + '_' + splitter[1] + '_' + outputFileNameSuffix
    o = open(outputFile, 'w+', encoding='utf8')
    personWriter = csv.writer(o, delimiter=',', lineterminator='\n')
    'READ IN SCHEDULE FILE'
    allTimes = read_schedule_files()
    count = -1
    'SCHEDULE EVERYONES DAILY ACTIVITY PATTERN'
    
    'Begin Reporting'
    startTime = datetime.now()
    print(state + " started at: " + str(startTime))
    writeHeaders(personWriter)
    
    'ASSIGN EACH RESIDENT WITHIN THE COUNTY THEIR REVISED ACTIVITY PATTERN WITH NEW TIME ATTRIBUTES AND WRITE TO COUNTY FILE'
    for r in reader:
        if count == -1: count+=1; continue
        activityPattern = r[6]
        'Initialize New Trip Sequence, Adding Spots for oTime and dTime'
        personalActivity = initialize_new_activityPattern(r[7:])
        personalActivity = scheduleDay(personalActivity, allTimes, activityPattern)
        count += 1
        if len(r[3]) == 4:
            r[3] = '0' + r[3]
        personWriter.writerow([r[0]] + [r[1]] + [r[2]] + [r[3]] + [r[4]] + [r[5]] + [r[6]] +
                              [personalActivity[0][0]] + [personalActivity[0][1]] + [personalActivity[0][2]] + [personalActivity[0][3]] + [personalActivity[0][4]] + [personalActivity[0][5]] + [personalActivity[0][6]] + [personalActivity[0][8]] + [personalActivity[0][9]] +
                              [personalActivity[1][0]] + [personalActivity[1][1]] + [personalActivity[1][2]] + [personalActivity[1][3]] + [personalActivity[1][4]] + [personalActivity[1][5]] + [personalActivity[1][6]] + [personalActivity[1][8]] + [personalActivity[1][9]] +
                              [personalActivity[2][0]] + [personalActivity[2][1]] + [personalActivity[2][2]] + [personalActivity[2][3]] + [personalActivity[2][4]] + [personalActivity[2][5]] + [personalActivity[2][6]] + [personalActivity[2][8]] + [personalActivity[2][9]] +
                              [personalActivity[3][0]] + [personalActivity[3][1]] + [personalActivity[3][2]] + [personalActivity[3][3]] + [personalActivity[3][4]] + [personalActivity[3][5]] + [personalActivity[3][6]] + [personalActivity[3][8]] + [personalActivity[3][9]] +
                              [personalActivity[4][0]] + [personalActivity[4][1]] + [personalActivity[4][2]] + [personalActivity[4][3]] + [personalActivity[4][4]] + [personalActivity[4][5]] + [personalActivity[4][6]] + [personalActivity[4][8]] + [personalActivity[4][9]] +
                              [personalActivity[5][0]] + [personalActivity[5][1]] + [personalActivity[5][2]] + [personalActivity[5][3]] + [personalActivity[5][4]] + [personalActivity[5][5]] + [personalActivity[5][6]] + [personalActivity[5][8]] + [personalActivity[5][9]] +
                              [personalActivity[6][0]] + [personalActivity[6][1]] + [personalActivity[6][2]] + [personalActivity[6][3]] + [personalActivity[6][4]] + [personalActivity[6][5]] + [personalActivity[6][6]] + [personalActivity[6][8]] + [personalActivity[6][9]])
        if count % 100000 == 0:
            print(str(count) + ' Residents Completed and taken this much time: ' + str(datetime.now()-startTime))
    f.close()
    o.close()  
    print(str(count) + ' of all Residents in ' + filename + ' have been processed')
    print(filename + " took this much time: " + str(datetime.now()-startTime))


'ASSIGN ALL TRIP TOURS THEIR TEMPORAL ATTRIBUTES' 
'RUN BY STATE, WHICH READS ALL COUNTY FILES IN STATE FOLDER'
def state_run(state):
    mypath = rootFilePath + 'Module 5\\' + state + '\\'
    onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
    for j in onlyfiles:
        executive(j, state)

import sys
exec('state_run(sys.argv[1])')