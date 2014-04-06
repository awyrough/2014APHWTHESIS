"""
workPlaceHelper.py

Project: United States Trip File Generation - Module 2
Author: A.P. Hill Wyrough
version date: 3/23/14
Python 3.3

PURPOSE: This set of methods and classes provides operations enabling the selection of a work place for a worker. It reads in employment files
for a particular county, creates lists of employers by industry, and provides classes for creating distributions and selecting employers. 

Relies on access to Emp Pat Files For All States and All counties

DEPENDENCIES: industryReader.py; countyAdjacencyReader.py

NOTE: This is all original work, none of these methods are taken from Mufti's Module 2, as they are performed entirely in a new fashion.
"""

""" Initialize a work county and return the entire object """
import industryReader
import countyAdjacencyReader
import random
import bisect

'Working County Object - To Hold All Emp-Pat Data For a Given County'
class workingCounty:
    'Initialize with FIPS'
    def __init__(self, fips):
        self.data = industryReader.read_county_employment(fips)
        self.county = countyAdjacencyReader.read_data(fips)
        self.county.set_lat_lon()
        self.lat, self.lon = self.county.get_lat_lon()
        self.industries = []
        self.create_industryLists()
        self.distributions = []
        self.spots = []
        self.create_industry_distributions()
    'Print County For Testing Purposes'
    def printCounty(self):
        self.county.print_county()
    'Partition Employers/Patrons into Industries'
    def create_industryLists(self):
        agr = []; mqo = []; con = []; man = []; wtr = []; rtr = []
        tra = []; uti = []; inf = []; fin = []; rer = []; pro = []
        mgt = []; adm = []; edu = []; hea = []; art = []; aco = []
        otr = []; pub = []
        for j in self.data:
            if j[9][2:4] == 'NA': code = 99
            else: code = int(j[9][2:4])
            if (code == 11): agr.append(j)
            elif (code == 21): mqo.append(j)
            elif (code == 23): con.append(j)
            elif (code in [31, 32, 33]): man.append(j)
            elif (code == 42): wtr.append(j)
            elif (code in [44, 45]): rtr.append(j)
            elif (code in [48, 49]): tra.append(j)
            elif (code == 22): uti.append(j)
            elif (code == 51): inf.append(j)
            elif (code == 52): fin.append(j)
            elif (code == 53): rer.append(j)
            elif (code == 54): pro.append(j)
            elif (code == 55): mgt.append(j)
            elif (code == 56): adm.append(j)
            elif (code == 61): edu.append(j)
            elif (code == 62): hea.append(j)
            elif (code == 71): art.append(j)
            elif (code == 72): aco.append(j)
            elif (code == 81): otr.append(j)
            elif (code == 92): pub.append(j)
            else: otr.append(j)
        self.industries = [agr, mqo, con, man, wtr, rtr, tra, uti,
                           inf, fin, rer, pro, mgt, adm, edu, hea,
                           art, aco, otr, pub]     
        return
    
    'Create Distributions For Each Industry'
    def create_industry_distributions(self):
        distributions = []
        allSpots = []
        for j in self.industries:
            dist = []
            spots = []
            count = 0
            for k in j:
                dist.append([count, int(k[13][2:].strip("'")), float(k[15][2:].strip("'")), float(k[16][2:].strip("'"))])
                spots.append(int(k[13][2:].strip("'")))
                count += 1
            distributions.append(dist)
            allSpots.append(spots)
        self.distributions = distributions
        self.spots = allSpots
    
    'Create a Gravity Model Distribution, CDF, Then Selection Of Employer'
    def create_specific_distribution(self, dist, spots, homelat, homelon):
        'Get List of # of Workers, Calculate Distance From Home to all Employers'
        'Calculate Pre-Normalized Weighted List (# of workers / Dij^2) for all employers j in county i'
        drawList = spots_to_distances(dist, spots, homelat, homelon)
        if len(dist) == 0: print('ERROR')
        if sum(drawList) <= 0:
            if (len(drawList) - 1) > 0:
                idx = random.randint(0, len(drawList) - 1)
            else:
                idx = 0
            return(idx)
        'Calculate Normalization Factor: sum of (# of workers / Dij^2) for all employers j in county i'
        'Calculate Weighted, Normalized List'
        weightedList = weight_my_list(drawList)
        'Draw From Weighted List and Get Row Pointer of Employer'
        weights = industryReader.cdf(weightedList)
        x=random.random()
        idx=bisect.bisect(weights,x)
        'Return Row Pointer/Index'
        return idx
    
    'Selection of Industry and Employer for a Particular Resident, Given Work County and Demographic Data'
    def select_industry_and_employer(self, lat, lon, wC, gender, income, menemp, womemp, meninco, wominco):
        markers = []
        for j in (self.distributions):
            if len(j) == 0: 
                markers.append(True)
            else: 
                markers.append(False)
        indust, index = industryReader.get_work_industryA(wC, gender, income, menemp, womemp, meninco, wominco, markers)
        employer = self.select_employer(index, lat, lon, wC)
        return indust, index, employer    

def weight_my_list(drawList):
    normFactor = sum(drawList)
    weightedlist =  [x/normFactor for x in drawList]
    return weightedlist

def spots_to_distances(dist, spots, lat, lon):
    'Get List of # of Workers, Calculate Distance From Home to all Employers'
    'Calculate Pre-Normalized Weighted List (# of workers / Dij^2) for all employers j in county i'
    drawList = [float(s)/(countyAdjacencyReader.distance_between_points(lat, lon, j[2] , j[3])**2) for s, j in zip(spots, dist)]
    return drawList       
