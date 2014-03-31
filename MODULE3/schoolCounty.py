'''
schoolCounty.py

Project: United States Trip File Generation - Module 3
Author: A.P. Hill Wyrough
version date: 3/15/2014
Python 3.3

Purpose: This is the helper module for module3, which assigns each student a proper place of school. This module creates and designs a school County
object that houses all the enrollment data for a particular county and its geographical neighbors. It provides methods to select a county of schooling,
and then a particular school given that county and type of school.

Dependencies: None

Notes: 

'''

import countyAdjacencyReader
import csv
import math
import random
import bisect

'File Location of School Data'
schoolDataBase = "C:\\Users\\Hill\\Desktop\\Thesis\\Data\\Schools\\School Database\\"

'Create Cumulative Distribution'
def cdf(weights):
    total=sum(weights)
    result=[]
    cumsum=0
    for w in weights:
        cumsum+=w
        result.append(cumsum/total)
    return result

'SchoolCounty Object: An object for housing the entire school data for a particular county, and points to its neighbors. '
class schoolCounty:
    def __init__(self, fips):
        'Initialize County Geography'
        self.fips = fips
        self.county = countyAdjacencyReader.read_data(fips)
        self.county.set_lat_lon()
        'Read Post-Secondary Schools'
        self.twoyear, self.fouryear, self.nondeg = self.read_post_sec_schools_for_county(fips)
        'Read All Public Schools'
        self.elempublic, self.midpublic, self.highpublic = self.read_public_schools(fips)
        'Read All Private Schools'
        self.elemprivate, self.midprivate, self.highprivate = self.read_private_schools(fips)
        self.totalseats = self.get_total_seats()
        self.fouryeardist = []
        self.twoyeardist = []
        self.nondist = []
        self.neighborlyschools = []
        self.options = []
    
    'Find and Initialize Neighbors of Home County'
    def assemble_neighborly_dist(self, fips):
        neighborlyschools = []
        for j in self.county.neighbors:
            neighborlyschools.append(schoolCounty(j))
        self.neighborlyschools = neighborlyschools
        
    'Calculate the Total Enrollment of a County'
    def get_total_seats(self):
        seats = 0
        for k in self.elempublic:
            seats += int(k[5])
        for k in self.midpublic:
            seats += int(k[5])
        for k in self.highpublic:
            seats+= int(k[5])
        for k in self.elemprivate:
            seats += int(k[7])
        for k in self.midprivate:
            seats += int(k[7])
        for k in self.highprivate:
            seats+= int(k[7])
        return seats
    
    'Create a Distribution of All Counties relative to Home County'
    def school_county_dist(self):
        options = []
        idx = 0
        seats = 0
        for j in self.neighborlyschools:
            for k in j.elempublic:
                seats += int(k[5])
            for k in j.midpublic:
                seats += int(k[5])
            for k in j.highpublic:
                seats+= int(k[5])
            for k in j.elemprivate:
                seats += int(k[7])
            for k in j.midprivate:
                seats += int(k[7])
            for k in j.highprivate:
                seats +=int(k[7])
            options.append([idx, j.fips, seats, distance_between_counties(self.county.lat, self.county.lon, j.county.lat, j.county.lon)])
            seats = 0
            idx+=1
        self.options = options
        
    'Select A County of Schooling Given Home county and types'
    def select_school_county(self, type1, type2):  
        newOptions = []
        idx = 0
        seats = 0
        for j in self.neighborlyschools:
            if type2 == 'private':
                if type1 == 'elem':
                    if len(j.elemprivate) == 0: newOptions.append([idx, j.fips, 0, 1000])
                    else: newOptions.append(self.options[idx])
                elif type1 == 'mid':
                    if len(j.midprivate) == 0: newOptions.append([idx, j.fips, 0, 1000])
                    else: newOptions.append(self.options[idx])
                elif type1 == 'high':
                    if len(j.highprivate) == 0: newOptions.append([idx, j.fips, 0, 1000])
                    else: newOptions.append(self.options[idx])
            elif type2 == 'public':
                if type1 == 'elem':
                    if len(j.elempublic) == 0: newOptions.append([idx, j.fips, 0, 1000])
                    else: newOptions.append(self.options[idx])
                elif type1 == 'mid':
                    if len(j.midpublic) == 0: newOptions.append([idx, j.fips, 0, 1000])
                    else: newOptions.append(self.options[idx])
                elif type1 == 'high':
                    if len(j.highpublic) == 0: newOptions.append([idx, j.fips, 0, 1000])
                    else: newOptions.append(self.options[idx])
            else:
                newOptions.append(self.options[idx])
            idx += 1
        dists = [float(j[2]) / j[3]**2 for j in newOptions]
        allDistances = []
        [allDistances.append(j[3]) for j in newOptions]
        if type2 == 'private':
            if type1 == 'elem': 
                if len(self.elemprivate) != 0:
                    dists.append(float(self.totalseats) / (min(allDistances) * 0.750)**2)
            elif type1 == 'mid':
                if len(self.midprivate) != 0:
                    dists.append(float(self.totalseats) / (min(allDistances) * 0.750)**2)
            elif type1 == 'high':
                if len(self.highprivate) != 0:
                    dists.append(float(self.totalseats) / (min(allDistances) * 0.750)**2)
        if type2 == 'public':
            if type1 == 'elem': 
                if len(self.elempublic) != 0:
                    dists.append(float(self.totalseats) / (min(allDistances) * 0.750)**2)
            elif type1 == 'mid':
                if len(self.midpublic) != 0:
                    dists.append(float(self.totalseats) / (min(allDistances) * 0.750)**2)
            elif type1 == 'high':
                if len(self.highpublic) != 0:
                    dists.append(float(self.totalseats) / (min(allDistances) * 0.750)**2)
        if sum(dists) == 0:
            return 'change'
        if sum(dists) != 0:
            dists = [j / sum(dists) for j in dists]
        weights = cdf(dists)
        split = random.random()
        idx=bisect.bisect(weights,split)
        if idx == len(self.options):
            return ('home county')
        else:
            return (self.neighborlyschools[idx])
        
    'For Each Post-Secondary School List, Scale The Employee Numbers to Student Enrollment'
    def scale_school_employment_to_students(self, statefouryear, statetwoyear, statenodeg):
        countyfouryear, countytwoyear, countynodeg = get_scale_factor(self.fips, self.county.statecode, statefouryear, statetwoyear, statenodeg)
        totalEmployment = []
        [totalEmployment.append(int(j[len(j) - 4])) for j in self.fouryear]
        totalFourEmployment = sum(totalEmployment)
        totalEmployment = []        
        [totalEmployment.append(int(j[len(j) - 4])) for j in self.twoyear]
        totalTwoEmployment = sum(totalEmployment)
        totalEmployment = []
        [totalEmployment.append(int(j[len(j) - 4])) for j in self.nondeg]
        totalNonEmployment = sum(totalEmployment)
        count = 0
        fouryeardist = []; twoyeardist = []; nondist = []
        for j in self.fouryear:
            j[len(j) - 4] = int((float(j[len(j) - 4]) / totalFourEmployment) * countyfouryear)
            fouryeardist.append([count, j[len(j) - 4]])
            count+=1
        count = 0
        for j in self.twoyear:
            j[len(j) - 4] = int((float(j[len(j) - 4]) / totalTwoEmployment) * countytwoyear)
            twoyeardist.append([count, j[len(j) - 4]])
            count+=1
        count = 0
        for j in self.nondeg:
            j[len(j) - 4] = int((float(j[len(j) - 4]) / totalNonEmployment) * countynodeg)
            nondist.append([count, j[len(j) - 4]])
            count+=1
        self.fouryeardist = fouryeardist
        self.twoyeardist = twoyeardist
        self.nondist = nondist
        return fouryeardist, twoyeardist, nondist
       
    'Select an Individual School For a Student' 
    def get_school_by_type(self, type1, type2):
        if type1 == 'elem' or type1 == 'mid' or type1 == 'high':
            county = self.select_school_county(type1, type2)
            if county == 'change':
                type2 = 'public'
                county = self.select_school_county(type1, type2)
            if county == 'change':
                return 0
            if type2 == 'public':
                if type1 == 'elem':
                    if county == 'home county': school = drawSchool(self.elempublic)
                    else: school = drawSchool(county.elempublic)
                elif type1 == 'mid':
                    if county == 'home county': school = drawSchool(self.midpublic)
                    else: school = drawSchool(county.midpublic)
                elif type1 == 'high':
                    if county == 'home county': school = drawSchool(self.highpublic)
                    else: school = drawSchool(county.highpublic)
            elif type2 == 'private':  
                if type1 == 'elem':
                    if county == 'home county': school = drawSchool(self.elemprivate)
                    else: school = drawSchool(county.elemprivate)
                elif type1 == 'mid':
                    if county == 'home county': school = drawSchool(self.midprivate)
                    else: school = drawSchool(county.midprivate)
                elif type1 == 'high':
                    if county == 'home county': school = drawSchool(self.highprivate)
                    else: school = drawSchool(county.highprivate)
        elif type1 == 'college' or type1 == 'on campus college':
            if type2 == 'four year':
                try:
                    school = self.drawCollege(self.fouryeardist, self.fouryear)
                except (ZeroDivisionError, IndexError): 
                    for j in self.neighborlyschools:
                        try:
                            school = j.drawCollege(j.fouryeardist, j.fouryear)
                            break
                        except (ZeroDivisionError, IndexError):
                            test = True
            elif type2 == 'two year':
                try:
                    school = self.drawCollege(self.twoyeardist, self.twoyear)
                except (ZeroDivisionError, IndexError):
                    for j in self.neighborlyschools:
                        try:
                            school = j.drawCollege(j.fouryeardist, j.fouryear)
                            break
                        except (ZeroDivisionError, IndexError):
                            test = True
            elif type2 == 'non deg':
                try:
                    school = self.drawCollege(self.nondist, self.nondeg)
                except(ZeroDivisionError, IndexError):
                    for j in self.neighborlyschools:
                        try:
                            school = j.drawCollege(j.nondist, j.nondeg)
                            break
                        except (ZeroDivisionError, IndexError):
                            test = True
        elif type1 == 'non student':
            return 1
        else:
            return 0
        try:
            return school
        except UnboundLocalError:
            return 0
    
    'Draw College Institution From List'
    def drawCollege(self, schoolList, schools):
        weights= []
        [weights.append(j[1]) for j in schoolList]
        cdf2 = cdf(weights)
        split = random.random()
        idx = bisect.bisect(cdf2, split)
        return schools[idx]
    
    'Initialize Public Schools For County'
    def read_public_schools(self, fips):
        fileLocationElem = schoolDataBase + 'CountyPublicSchools\\' +  'Elem\\'
        fileLocationMid = schoolDataBase + 'CountyPublicSchools\\' +  'Mid\\'
        fileLocationHigh = schoolDataBase + 'CountyPublicSchools\\' +  'High\\'
        try:
            elem = open(fileLocationElem + fips + 'Elem.csv', 'r')
            elempublicschools = csv.reader(elem, delimiter = ',')
        except IOError:
            elem = None
        try:
            mid = open(fileLocationMid + fips + 'Mid.csv', 'r')
            midpublicschools = csv.reader(mid, delimiter = ',')
        except IOError:
            mid = None
        try:
            high = open(fileLocationHigh + fips + 'High.csv', 'r')
            highpublicschools = csv.reader(high, delimiter = ',')
        except IOError:
            high = None
        elempublic = []; midpublic = []; highpublic = []
        if elem != None:
            [elempublic.append(row) for row in elempublicschools]
        if mid != None:
            [midpublic.append(row) for row in midpublicschools]
        if high != None:
            [highpublic.append(row) for row in highpublicschools]
        return elempublic, midpublic, highpublic

    'Initialize Private Schools For County'
    def read_private_schools(self, fips):
        fileLocation = schoolDataBase + 'CountyPrivateSchools\\'
        try:
            elem = open(fileLocation + fips + 'Private.csv', 'r')
            elemprivateschools = csv.reader(elem, delimiter = ',')
        except IOError:
            elem = None
        elemprivate = []; midprivate = []; highprivate = []
        if elem != None:
            for row in elemprivateschools:
                if row[6] == '1':
                    elemprivate.append(row)
                if row[6] == '2' or row[6] == '3':
                    highprivate.append(row)
        midprivate = highprivate
        return elemprivate, highprivate, highprivate    
   
    'Initialize Post Secondary Schools for county'
    def read_post_sec_schools_for_county(self, fips):
        countyAbbrev = self.county.stateabbrev
        fileLocation = schoolDataBase + 'PostSecSchoolsByCounty\\' + countyAbbrev + '\\' + str(fips) + '_' + countyAbbrev + '_'
        try:
            twoyear = open(fileLocation + 'CommunityCollege.csv', 'r')
            twoyearschools = csv.reader(twoyear, delimiter=',')
        except IOError:
            twoyear = None
        try:
            fouryear = open(fileLocation + 'University.csv', 'r')
            fouryearschools = csv.reader(fouryear, delimiter=',')
        except IOError:
            fouryear = None
        try:
            nondeg = open(fileLocation + 'NonDegree.csv', 'r')
            nondegschools = csv.reader(nondeg, delimiter=',')
        except IOError:
            nondeg = None
        allNonDegSchools = []; allTwoYearSchools = []; allFourYearSchools = []
        if twoyear != None:
            for row in twoyearschools: allTwoYearSchools.append(row)
        if fouryear != None:
            for row in fouryearschools: allFourYearSchools.append(row)
        if nondeg != None:
            for row in nondegschools: allNonDegSchools.append(row)
        return allTwoYearSchools, allFourYearSchools, allNonDegSchools

'SELECT (NON-SECONDARY) SCHOOL FROM LIST USING ASSEMBLED DISTIRBUTION'
def drawSchool(schoolList):
    weights = []
    if len(schoolList[0]) == 10:
        [weights.append(float(j[5])) for j in schoolList]
    else:
        [weights.append(float(j[7])) for j in schoolList]
    cdf2 = cdf(weights)
    split = random.random()
    idx = bisect.bisect(cdf2, split)
    return schoolList[idx]

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

'Scale State Enrollment in Types of Post-Sec Schools by County Population'
'To Obtain County Enrollment in Different Programs'
def get_scale_factor(fips, state, statefouryear, statetwoyear, statenodeg):
    statecounties = []
    C_PATH = "C:\\Users\\Hill\\Desktop\\Thesis\\Data\\WorkFlow"
    fname = C_PATH + '\\allCounties.txt'
    f = open(fname, 'r+')
    totalStatePop = 0.0
    countyPop = []
    weights = []
    for line in f:
        splitter = line.split(',')
        'In State'
        if (splitter[1] == state):
            if splitter[3] not in statecounties:
                statecounties.append(splitter[3])
                totalStatePop+=float(splitter[7])
                countyPop.append([splitter[3], splitter[7]])
    for j in countyPop:
        weights.append([j[0], float(j[1])/totalStatePop])
        if j[0] == fips:
            req = (weights.pop())
    countyfouryear = req[1]*statefouryear
    countytwoyear = req[1]*statetwoyear
    countynodeg = req[1]*statenodeg
    return countyfouryear, countytwoyear, countynodeg


#countyPop = get_scale_factor('10003', '10', 10000, 20000 ,1500)
#print(countyPop)

#test.scale_school_employment_to_students(0, 0, 0)
#for row in test.fouryear:
#    print(row)
#test.county.print_county()