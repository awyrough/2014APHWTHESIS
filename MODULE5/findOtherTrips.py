import classDumpModule5
import numpy
import random
import bisect
'----------PATH DEFINITIONS---------------------'
rootDrive = 'E'
rootFilePath = rootDrive + ':\\Thesis\\Output\\'
inputFileNameSuffix = 'Module4NN2ndRun.csv'
outputFileNameSuffix = 'Module5NN1stRun.csv'

dataDrive = 'E'
dataRoot = dataDrive + ':\\Thesis\\Data\\'
'-----------------------------------------------'
def populateActivities(personalTour, person, homeCountyPatronage, state, countyNameData):
    'Find Other Trips'
    count = 0
    trips = []
    for j in personalTour.activityPattern[2]:
        if j[0] == 'O':
            trips.append(count)
        count += 1
    for j in range(0,len(trips)):
        otherTrip = (personalTour.activities[trips[j]])
        'Get County of Start of Trip'
        if otherTrip[2] == 'H':
            originCounty = personalTour.activities[0][5]
            prev = 'H'
        elif otherTrip[2] == 'W':
            originCounty = personalTour.activities[trips[j] - 1][5]
            prev = 'W'
        elif otherTrip[2] == 'O':
            originCounty = personalTour.activities[trips[j] - 1][5]
            prev = 'O'
        elif otherTrip[2] == 'S':
            originCounty = personalTour.activities[trips[j] - 1][5]
            prev = 'S'
        'Determine Work-Work Trip (because of restriction)'
        marker = False
        if otherTrip[2] == 'W' and otherTrip[3] == 'W': marker = True
        startLon = personalTour.activities[trips[j] - 1][6]
        startLat = personalTour.activities[trips[j] - 1][7]        
        
        name, countyName, lat, lon, indust, homeCountyPatronage = getOtherTrip(str(originCounty), startLon, startLat, marker, homeCountyPatronage, prev)

        personalTour.activities[trips[j]][4] = name
        personalTour.activities[trips[j]][5] = classDumpModule5.lookup_name(countyName, state, countyNameData)
        personalTour.activities[trips[j]][6] = lat
        personalTour.activities[trips[j]][7] = lon
        personalTour.activities[trips[j]][8] = indust
    
    return personalTour, homeCountyPatronage

def getOtherTrip(originCounty, startLon, startLat, marker, homeCountyPatronage, prev):
    count = 0
    index = -1
    if prev == 'H': sets = homeCountyPatronage.homeCounties
    elif prev == 'S': sets = homeCountyPatronage.schoolCounties
    elif prev == 'W': sets = homeCountyPatronage.workCounties
    else: sets = homeCountyPatronage.otherCounties
    for j in sets:
        if originCounty == j.FIPS:
            index = count
            break
    if index == -1:
        if prev == 'H':
            homeCountyPatronage.homeCounties.append(patronageCounty(originCounty))
            index = len(homeCountyPatronage.homeCounties) - 1
            sets = homeCountyPatronage.homeCounties
        elif prev == 'S':
            homeCountyPatronage.schoolCounties.append(patronageCounty(originCounty))
            index = len(homeCountyPatronage.schoolCounties) - 1
            sets = homeCountyPatronage.schoolCounties
        elif prev == 'W':
            homeCountyPatronage.workCounties.append(patronageCounty(originCounty))
            index = len(homeCountyPatronage.workCounties) - 1
            sets = homeCountyPatronage.workCounties
        elif prev == 'O':
            homeCountyPatronage.otherCounties.append(patronageCounty(originCounty))
            index = len(homeCountyPatronage.otherCounties) - 1
            sets = homeCountyPatronage.otherCounties
    'County Patronage List'
    countyPatronage = sets[index]
    'Select Industry of Patronage'
    industry_weights = classDumpModule5.cdf(countyPatronage.patronCounts)
    split = random.random()
    idx = bisect.bisect(industry_weights, split)
    if countyPatronage.patronCounts[idx] > 5:
        countyPatronage.patronCounts[idx]-=1
    lists = countyPatronage.industries[idx]
    'Select Particular Place of Patronage'
    allDistances = []
    'Note: Restrictons on Geography are built into distance calculations'
    if marker == False:
        [allDistances.append(float(j[12]) / (classDumpModule5.distance_between_points_normal(startLon, startLat, float(j[15]), float(j[16].strip('\n')))**2)) for j in lists]
    else:
        [allDistances.append(float(j[12]) / (classDumpModule5.distance_between_points_w2w(startLon, startLat, float(j[15]), float(j[16].strip('\n')))**2)) for j in lists]
    try:
        norm = sum(allDistances)
        [j/norm for j in allDistances]
    except ZeroDivisionError:
        [j/1.0 for j in allDistances]
    if sum(allDistances) == 0:
        index = random.randint(0, len(allDistances) - 1)
    else:
        weights = classDumpModule5.cdf(allDistances)
        split = random.random()
        index = bisect.bisect(weights, split)
    if int(countyPatronage.industries[idx][index][12]) > 1:
        countyPatronage.industries[idx][index][12] = int(countyPatronage.industries[idx][index][12]) - 1
    patronagePlace = lists[index]
    'Return Other Trip Information'
    name = patronagePlace[0]
    county = patronagePlace[5]
    lat = float(patronagePlace[len(patronagePlace) - 2])
    lon = float(patronagePlace[len(patronagePlace) - 1].strip('\n'))
    indust = patronagePlace[9][0:2]
    return name, county, lat, lon, indust, homeCountyPatronage

class patronageCounty:
    'Initialize with FIPS'
    def __init__(self, fips):
        self.data = read_county_employment((fips))
        self.FIPS = str(fips)
        self.industries = []
        self.patronCounts = []
        self.create_industryLists()
        self.distributions = []
        self.spots = []
    'Partition Employers/Patrons into Industries'
    def create_industryLists(self):
        agr = []; mqo = []; con = []; man = []; wtr = []; rtr = []
        tra = []; uti = []; inf = []; fin = []; rer = []; pro = []
        mgt = []; adm = []; edu = []; hea = []; art = []; aco = []
        otr = []; pub = []
        agrCount = 0; mqoCount = 0; conCount = 0; manCount = 0; wtrCount = 0;
        rtrCount = 0; traCount = 0; utiCount = 0; infCount = 0; finCount = 0;
        rerCount = 0; proCount = 0; mgtCount = 0; admCount = 0; eduCount = 0;
        heaCount = 0; artCount = 0; acoCount = 0; otrCount = 0; pubCount = 0;
        for j in self.data:
            if j[9] == 'NA': code = 99
            else: code = int(j[9][0:2])
            
            'Deal With Scientific Notation'
            number = (j[12])
            if len(number) == 8:
                if number[len(number) - 3] == '+': 
                    number = 10000
            else:
                number = int(j[12])
            if (code == 11): agr.append(j); agrCount+=number
            elif (code == 21): mqo.append(j); mqoCount+=number
            elif (code == 23): con.append(j); conCount+=number
            elif (code in [31, 32, 33]): man.append(j); manCount+=number
            elif (code == 42): wtr.append(j); wtrCount+=number
            elif (code in [44, 45]): rtr.append(j); rtrCount+=number
            elif (code in [48, 49]): tra.append(j); traCount+=number
            elif (code == 22): uti.append(j); utiCount+=number
            elif (code == 51): inf.append(j); infCount+=number
            elif (code == 52): fin.append(j); finCount+=number
            elif (code == 53): rer.append(j); rerCount+=number
            elif (code == 54): pro.append(j); proCount+=number
            elif (code == 55): mgt.append(j); mgtCount+=number
            elif (code == 56): adm.append(j); admCount+=number
            elif (code == 61): edu.append(j); eduCount+=number
            elif (code == 62): hea.append(j); heaCount+=number
            elif (code == 71): art.append(j); artCount+=number
            elif (code == 72): aco.append(j); acoCount+=number
            elif (code == 81): otr.append(j); otrCount+=number
            elif (code == 92): pub.append(j); pubCount+=number
            else: otr.append(j); otrCount+=number
        self.industries = [agr, mqo, con, man, wtr, rtr, tra, uti,
                           inf, fin, rer, pro, mgt, adm, edu, hea,
                           art, aco, otr, pub]     
        self.patronCounts = [int(agrCount), int(mqoCount), int(conCount), int(manCount), wtrCount, rtrCount, traCount, utiCount,
                           infCount, finCount, rerCount, proCount, mgtCount, admCount, eduCount, heaCount,
                           int(artCount), int(acoCount), otrCount, pubCount] 
        return 
    
class patronageWarehouse:
    def __init__(self):
        self.homeCounties = []
        self.workCounties = []  
        self.schoolCounties = []
        self.otherCounties = []  
    
'Read in County Employment/Patronage File and Return List of All Locations in that county'
def read_county_employment(fips):
    if len(fips) == 4:
        fips = '0' + fips
    states = classDumpModule5.read_states()
    abbrev = classDumpModule5.match_code_abbrev(states, fips[0:2])
    filepath = dataRoot + 'Employment\\CountyEmployeeFiles\\' + abbrev + '\\' + fips + '_' + abbrev + '_EmpPatFile.csv'
    f = open(filepath, 'r+')
    data = []
    [data.append(row.split(',')) for row in f]
    return data
