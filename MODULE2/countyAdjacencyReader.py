'METHODOLOGY FOR THE HANDLING OF COUNTY OBJECTS, COUNTY LEVEL DATA, JOURNEY TO WORK (COUNTY TO COUNTY)'
'CALCULATING DISTANCE BETWEEN TWO COUNTIES'

import math
import random
import numpy as np

class County: 
    def __init__(self, name, stateabbrev, statecode, fipscode, countycode):
        self.name = name
        self.stateabbrev = stateabbrev
        self.statecode = fipscode
        self.fipscode = statecode
        self.countycode = countycode
        self.lat = 0
        self.lon = 0
        self.neighbors = []
        self.num = 0
    def add_neighbor(self, county):
        self.neighbors.append(county.fipscode)   
    def get_lat_lon(self):
        return self.lat, self.lon
    def get_num(self):
        return self.num
    def print_county(self):
        print('County name: ' + str(self.name))
        print('State Abbrev and Code: ' + str(self.stateabbrev) + ' ' + str(self.statecode))
        print('FipsCode: ' + str(self.fipscode))
        print('County Code: ' + str(self.countycode))
        print('Neighbors: ' + str(self.neighbors))
'RETURN LAT LON OF COUNTY BY FIPSCODE - POP/AREA DATA AVAILABLE'    
def read_counties(fipscode):
    'MAIN PATH ON MY COMPUTER TOWARDS FILES OF USE'
    M_PATH = "C:\\Users\\Hill\\Desktop\\Thesis\\Data\\WorkFlow"
    fname = M_PATH + '\\allCounties.csv'
    f = open(fname, 'r+')
    for line in f:
        splitter = line.split(',')
        if (splitter[3] == fipscode):
            return splitter[4], splitter[5]
'RETURN COUNTY OBJECT FOR GIVEN FIPS COUNTY CODE'       
def read_data(returncode):
    'MAIN PATH ON MY COMPUTER TOWARDS FILES OF USE'
    M_PATH = "C:\\Users\\Hill\\Desktop\\Thesis\\Data\\WorkFlow"
    fname = M_PATH + '\\county_adjacency.csv'
    f = open(fname, 'r+')
    count = 0
    list1 = []
    printcount = 0
    for line in f:
        count += 1
        condensed = (''.join(line.split()))
        splitter = condensed.split(',')
        countyname = splitter[0]
        stateabbrev = splitter[1][0:2]
        fipscode = splitter[1][2:7]
        statecode = splitter[1][2:4]
        countycode = splitter[1][4:7]
        if (splitter[2] != '') and (count == 1):
            homecounty = County(countyname, stateabbrev, fipscode, statecode, countycode)
            list1.append(homecounty.fipscode)
            homename = countyname
        elif (splitter[2] != '') and (count != 1):
            if (returncode == homecounty.fipscode): return homecounty
            homecounty = County(countyname, stateabbrev, fipscode, statecode, countycode)
            list1.append(homecounty.fipscode)
            homename = countyname
            if (splitter[1][7:] != countyname):
                firstneighborcountyname = splitter[1][7:]
                nstateabbrev = splitter[2][0:2]
                nfipscode = splitter[2][2:]
                nstatecode = splitter[2][2:4]
                ncountycode = splitter[2][4:]
                firstneighbor = County(firstneighborcountyname, nstateabbrev, nfipscode, nstatecode, ncountycode)
                homecounty.add_neighbor(firstneighbor)
        else:
            neighborcounty = County(countyname, stateabbrev, fipscode, statecode, countycode)
            if (countyname != homename):
                homecounty.add_neighbor(neighborcounty)
        if count == 21721:
            printcount+=1
            homecounty.print_county()
    return homecounty
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
    return arc*3963.1676 
'RETURN DISTANCE BETWEEN TWO COUNTIES BY FIPS CODE'
def get_distance(fips1, fips2):
    lat1, lon1 = read_counties(fips1)
    lat2, lon2 = read_counties(fips2)
    dist = distance_between_counties(lat1, lon1, lat2, lon2)
    return dist
'READ JOURNEY TO WORK CENSUS'
def read_J2W():
    'MAIN PATH ON MY COMPUTER TOWARDS FILES OF USE'
    M_PATH = "C:\\Users\\Hill\\Desktop\\Thesis\\Data\\WorkFlow"
    fname = M_PATH + '\\J2W.txt'
    f = open(fname, 'r+')
    allJ2W = []
    for line in f:
        allJ2W.append(line)
    return allJ2W[1:]
'GET ALL COUNTY to COUNTY MOVEMENTS FOR GIVEN COUNTY BY FIPS CODE, LIST OF COUNTY-COUNTY [FIPSHOME, FIPSWORK, #]'
def get_movements(fipscode, data):
    array = []
    for i, j in enumerate(data):
        splitter = j.split(',')
        fips = (splitter[0]+splitter[1])
        if (fips == fipscode):
            array.append(splitter)
    newarray = []
    for i, j in enumerate(array):
        newarray.append([j[2]+j[3], j[4]])
    return newarray

'GIVEN ARRAY OF ALL MOVEMENTS FROM A COUNTY, GENERATE A DISTRIBUTION WHEREBY'
def create_distribution(movearray):
    newarray = []
    for i, j in enumerate(movearray):
        newarray.append([j[1], j[2]])
    return newarray

'JOURNEY TO WORK FLOW OBJECT AND CLASS OPERATIONS'       
class j2wDist:
    def __init__(self, array):
        self.flows = array
        self.items = []
        self.vals = []
    def get_pairs(self):
        return create_distribution(self.flows)
    def get_items(self):
        items = []
        values = []
        for j in self.flows:
            items.append(j[0])
            values.append(int(j[1]))
        self.items = items
        self.vals = values
        return items, values
    def total_workers(self):
        return sum(self.vals)
    def select(self):
        variate = random.random() * sum(self.vals)
        cum = 0.0
        count = 0
        for it in self.items:
            cum += self.vals[count]
            if variate < cum:
                self.vals[count]-=1
                return it
            count += 1
        return it
        
        
        
        
        
'TESTING'
data = read_J2W()
array = get_movements('11001', data)
#newarray = create_distribution(array)
#print(array)
#print(newarray)

testDist = j2wDist(array)

#print(testDist.get_pairs())

items, vals = testDist.get_items()


