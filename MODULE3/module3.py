'''
module3.py

Project: United States Trip File Generation - Module 3
Author: A.P. Hill Wyrough
version date: 3/15/2014
Python 3.3

Purpose: This is the executive function for Task 3 (Module 3) that assigns a school to every resident that is of a school age, or attends college. 

Dependencies: schoolCounty.py

Notes: This procedure, because of its national scale, is entirely different than Mufti's statewide designations of community or non-community schools. 

'''

from datetime import datetime
import schoolCounty
import csv
import random
import bisect

'Direction of School Data Base'
schoolDataBase = "C://Users//Hill//Desktop//Thesis//Data//Schools//School Database//"

'Constants for National Enrollment in Private and Public Schools'
public_school_enrollment_elem_mid = 34637.0
public_school_enrollment_high = 14668.0
private_school_enrollment_elem_mid = 4092.0
private_school_enrollment_high = 1306.0      
total = public_school_enrollment_elem_mid + public_school_enrollment_high + private_school_enrollment_elem_mid + private_school_enrollment_high
privtotal = private_school_enrollment_elem_mid + private_school_enrollment_high
pubtotal = public_school_enrollment_elem_mid + public_school_enrollment_high

'Using National Percentages of Enrollment in Private vs. Public, Use Ratios to Scale State Enrollment in Each'
def scale_public_and_private(projHigh, projElemMid):
    # NATIONAL NUMBERS TO BE SCALED TO STATE LEVEL NUMBERS
    elemmidtotal  = private_school_enrollment_elem_mid + public_school_enrollment_elem_mid 
    hightotal =  + public_school_enrollment_high + private_school_enrollment_high
    # PROJECTED STATE LEVEL NUMBERS FOR ENROLLMENT IN ALL SCHOOLS
    prop1 = private_school_enrollment_elem_mid / elemmidtotal
    prop2 = public_school_enrollment_elem_mid / elemmidtotal
    projectedPrivElemMid = prop1 * projElemMid
    projectedPublElemMid = prop2 * projElemMid
    prop1 = private_school_enrollment_high / hightotal
    prop2 = public_school_enrollment_high / hightotal
    projectedPrivHigh = prop1 * projHigh
    projectedPublHigh = prop2 * projHigh
    return projectedPrivElemMid, projectedPublElemMid, projectedPrivHigh, projectedPublHigh

'Read State Enrollment in Schools, Scaled Using Past Data'
def read_state_enrollment(state):
    fileLocation = schoolDataBase + 'statehighelemmidenrollment.csv'
    f = open(fileLocation, 'r+')
    for row in f:
        row = row.split(',')
        row = [row[x].strip('"') for x in range(0,(len(row)))]
        if row[0].strip('.').strip(' ') == state:
            statetotalenrollment2009 = float(row[8].strip('\n').strip('"'))
            statetotalenrollment2006 = float(row[1].strip('"'))
            statetotalenrollment2007 = float(row[4].strip('"'))
            statehighenrollment2006 = float(row[3].strip('"'))
            stateelemmidenrollment2006 = float(row[2].strip('"'))
            statehighenrollment2007 = float(row[6].strip('"'))
            stateelemmidenrollment2007 = float(row[5].strip('"'))
            prop1 = statehighenrollment2006 / statetotalenrollment2006
            prop2 = statehighenrollment2007 / statetotalenrollment2007
            projected2009high = ((prop1+prop2)/2.0) * statetotalenrollment2009
            prop1 = stateelemmidenrollment2006 / statetotalenrollment2006
            prop2 = stateelemmidenrollment2007 / statetotalenrollment2007
            projected2009elemmid = ((prop1+prop2)/2.0) * statetotalenrollment2009
            return projected2009high, projected2009elemmid
        
'Read Enrollment In State For Post-Secondary Schools by Type'        
def read_post_sec_enrollment(state):
    fileLocation = schoolDataBase + 'stateenrollmentindegrees.csv'
    f = open(fileLocation, 'r+', encoding = 'utf8')
    for row in f:
        row = row.split(',')
        if (row[0] == state):
            total = row[3]
            bachelor = row[4]
            graduate = row[5]
            associates = row[6].strip('\n')
            return float(total), float(bachelor)+float(graduate), float(associates), float(row[2])
        
'Create Cumulative Distribution'
def cdf(weights):
    total=sum(weights)
    result=[]
    cumsum=0
    for w in weights:
        cumsum+=w
        result.append(cumsum/total)
    return result
  
'Assign Student a Type of School (Private/Public) or (Elem, Mid, High, College) Based on Age/HHT/State'  
def get_school_type(age, gender, hht, homecounty, homestate, privelemmidpop, pubelemmidpop, privhighpop, pubhighpop,
                    fouryear, twoyear, nondeg):
    'Not A Student'
    if hht in [2,3,4,5,7,8] or age<5 or age>24:
        return 'non student', 'no', pubelemmidpop, privelemmidpop, pubhighpop, privhighpop, fouryear, twoyear, nondeg
    elif hht == 6:
        fouryear-=1
        return 'on campus college', 'four year', pubelemmidpop, privelemmidpop, pubhighpop, privhighpop, fouryear, twoyear, nondeg 
    elif hht in [0,1]:
        # 6 to 10 -> ELEMENTARY SCHOOL
        if age < 11:
            type = 'elem'
            puborpriv = random.random()
            totalPop = pubelemmidpop + privelemmidpop
            thresh = pubelemmidpop / totalPop
            if puborpriv < thresh: 
                pubelemmidpop-=1
                type2 = 'public'
            else:
                privelemmidpop-=1 
                type2 = 'private'
        # 11 to 13 -> MIDDLE SCHOOL
        elif age < 14:
            type = 'mid'
            puborpriv = random.random()
            totalPop = pubelemmidpop + privelemmidpop
            thresh = pubelemmidpop / totalPop
            if puborpriv < thresh: 
                pubelemmidpop-=1
                type2 = 'public'
            else:
                privelemmidpop-=1 
                type2 = 'private'
        # 14 - 18.5 -> MIDDLE SCHOOL (HALF ARE IN HIGH SCHOOL, HALF COLLEGE)
        elif age < 19:
            split = random.random()
            if split > 0.5:
                type = 'high'
            else: 
                type = 'college'; 
                fouryearprop = fouryear / (fouryear +twoyear + nondeg)
                split = random.random()
                if split < fouryearprop:
                    type2 = 'four year'
                    fouryear-=1
                else:
                    type2 = 'two year'
                    twoyear-=1
            if type == 'high':
                puborpriv = random.random()
                totalPop = pubhighpop + privhighpop
                thresh = pubhighpop / totalPop
                if puborpriv < thresh: 
                    pubhighpop-=1
                    type2 = 'public'
                else:
                    privhighpop-=1 
                    type2 = 'private'
        elif age >= 19:
            type = 'college'
            split = random.random()
            fouryearprop = fouryear/(fouryear +twoyear + nondeg)
            twoyearprop = twoyear/(fouryear +twoyear + nondeg)
            nonprop = 1.0 - fouryearprop - twoyearprop
            weights = cdf([fouryearprop, twoyearprop, nonprop])
            names = ['four year', 'two year', 'non deg']
            idx=bisect.bisect(weights,split)
            type2 = names[idx]
            if idx == 0: fouryear-=1
            elif idx == 1: twoyear-=1
            else: nondeg-=1
        return type, type2, pubelemmidpop, privelemmidpop, pubhighpop, privhighpop, fouryear, twoyear, nondeg
        
'------------------------------------------------------------------------------------'
'WRITE MODULE 2 OUTPUT HEADERS'
def writeHeaders(pW):
    pW.writerow(['Residence State'] + ['County Code'] + ['Tract Code'] + ['Block Code'] + ['HH ID'] + ['HH TYPE'] + ['Latitude'] + ['Longitude'] 
                + ['Person ID Number'] + ['Age'] + ['Sex'] + ['Traveler Type'] + ['Income Bracket']
                + ['Income Amount'] + ['Work County'] + ['Work Industry'] + ['Employer'] + ['Work Address'] + ['Work City'] + ['Work State'] 
                + ['Work Zip'] + ['Work County Name'] + ['NAISC Code'] + ['NAISC Description'] + ['Patron:Employee'] + ['Patrons'] + ['Employees'] + ['Work Lat'] + ['Work Lon'] 
                + ['School Name'] + ['SchoolLat'] + ['SchoolLon'])

'ITERATE OVER ALL RESIDENTS WITHIN A STATE, ASSIGN SCHOOL IF QUALIFIED STUDENT'
def executive(state):
    'Module 3 Output Path'
    outputPath = "C:\\Users\\Hill\\Desktop\\Thesis\\Data\\Output\\Module3\\"
    'Module 2 Input Path'
    inputPath = "D:\\Thesis\\Output\\Module2 Output\\"
    'Begin Reporting'
    startTime = datetime.now()
    print(state + " started at: " + str(startTime))
    'OPEN STATE RESIDENCY FILE'
    fname = inputPath + state + 'Module2NN2ndRun.csv'
    f = open(fname, 'r')
    personReader = csv.reader(f , delimiter= ',')
    out = open(outputPath + str(state + 'Module3NN1stRun.csv'), 'w+', encoding='utf8')
    personWriter = csv.writer(out, delimiter=',', lineterminator='\n')
    writeHeaders(personWriter)
    trailingFIPS = ''

    'Gather State Enrollment Data'
    statehigh, stateelemmid = read_state_enrollment(state)
    privEleMidPop, pubEleMidPop, privHighPop, pubHighPop = scale_public_and_private(statehigh, stateelemmid)
    totalcollege, bachormore, assoc, non = read_post_sec_enrollment(state)
    '---------------------------RUN------------------------------------'
    specCount = 0
    studentCount = 0
    count= 0
    for row in personReader:
        if count == 0: count+=1; continue
        'Gather Personal Data of Resident'
        homeCounty = row[1]; homeState = row[0]; workCounty = row[14]
        age = int(row[9]); gender = int(row[10]); hht = int(row[5])
        'Update County of Residence, Prepare School County Object'
        if len(homeState+homeCounty) == 4:
            newCounty = '0'+homeState+homeCounty
        else:
            newCounty = homeState+homeCounty
        if newCounty != trailingFIPS:
            trailingFIPS = newCounty
            print(trailingFIPS)
            homecounty = schoolCounty.schoolCounty(trailingFIPS)
            homecounty.scale_school_employment_to_students(bachormore, assoc, non)
            homecounty.assemble_neighborly_dist(homecounty.fips)
            homecounty.school_county_dist()
        'FAIL-SAFE: REFRESH DISTRIBTION IF GOES TO ZERO'
        if bachormore == 0: totalcollege, bachormore, assoc, non = read_post_sec_enrollment(state)
        'Get School Type'
        type1, type2, pubEleMidPop, privEleMidPop, pubHighPop, privHighPop, bachormore, assoc, non = get_school_type(age, gender, hht, homeCounty, homeState, 
                                                                                                                     privEleMidPop, pubEleMidPop, privHighPop, pubHighPop,
                                                                                                                     bachormore, assoc, non)
        'Get School For Student'
        school = homecounty.get_school_by_type(type1, type2)
        'Gather Output From School Selected (Need to Deal With Different Formats of School Data'
        if school == 1 or school == 0:
            name = 'NA'
            schoollat = 'NA'
            schoollon = 'NA'
        else:
            if len(school) == 17:
                name = school[0]
                schoollat = school[15]
                schoollon = school[16]
            elif len(school) == 8:
                name = school[0]
                schoollat = school[4]
                schoollon = school[5]
            elif len(school) == 11:
                name = school[3]
                schoollat = school[6]
                schoollon = school[7]
            else:
                print(school)
        'Keep Track of Progress'
        if school == 0:
            specCount+=1
        elif school != 1:
            studentCount+=1
        count+=1
        'Write School Output' '(School name, county, Lat, Lon, Enrollment)'
        personWriter.writerow(row + [name] + [schoollat] + [schoollon])
    print(state + " took this much time: " + str(datetime.now()-startTime))
    print('students ' + str(studentCount))
    print('unassigned ' + str(specCount))
    print('pop ' + str(count))
import sys
exec('executive(sys.argv[1])')