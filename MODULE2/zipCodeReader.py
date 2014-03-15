'OBJECTIVE: READ IN ZIP CODE TO COUNTY FIPS AND CREATE A FILE WITH MATCHING DICTIONARY'
'ONLY NEEDED ONE TIME PRODUCES MATCHING DICTIONARY'
import employeePatronageReader
import csv

M_PATH = "C:\\Users\\Hill\\Desktop\\Thesis\\Data\\"

def match_abbrev_code(states, abbrev):
    for i, j in enumerate(states):
        splitter = j.split(',')
        if splitter[1] == abbrev:
            return splitter[2]
        
'READ IN ASSOCIATED STATE ABBREVIATIONS WITH STATE FIPS CODES'
def read_zips():
    states = employeePatronageReader.read_states()
    zipFileLocation = M_PATH + '\\ZipCodes\\'
    fname = zipFileLocation + 'zipcty1.txt'
    hname = zipFileLocation + 'zipCountyDictionary.csv'
    h = open(hname, 'w+', encoding='utf8')
    personWriter = csv.writer(h, delimiter= ',', lineterminator = '\n')
    f = open(fname, 'r+')
    trailingzip = '00000'
    for row in f:
        zipcode = row[0:5]
        if (zipcode != trailingzip):
            statecode = match_abbrev_code(states, row[23:25])
            if (statecode == None):
                continue
            countycode = row[25:28]
            fips = statecode + countycode
            personWriter.writerow([zipcode] + [fips])
            trailingzip = zipcode
            
    f.close()
    fname = zipFileLocation + 'zipcty4.txt'
    print(fname)
    f = open(fname, 'r+')
    for row in f:
        zipcode = row[0:5]
        if (zipcode != trailingzip):
            statecode = match_abbrev_code(states, row[23:25])
            if (statecode == None):
                continue
            countycode = row[25:28]
            fips = statecode + countycode
            personWriter.writerow([zipcode] + [fips])
            trailingzip = zipcode
    f.close()
    fname = zipFileLocation + 'zipcty5.txt'
    print(fname)
    f = open(fname, 'r+')
    for row in f:
        zipcode = row[0:5]
        if (zipcode != trailingzip):
            statecode = match_abbrev_code(states, row[23:25])
            if (statecode == None):
                continue
            countycode = row[25:28]
            fips = statecode + countycode
            personWriter.writerow([zipcode] + [fips])
            trailingzip = zipcode
    f.close()
    fname = zipFileLocation + 'zipcty6.txt'
    print(fname)
    f = open(fname, 'r+')
    for row in f:
        zipcode = row[0:5]
        if (zipcode != trailingzip):
            statecode = match_abbrev_code(states, row[23:25])
            if (statecode == None):
                continue
            countycode = row[25:28]
            fips = statecode + countycode
            personWriter.writerow([zipcode] + [fips])
            trailingzip = zipcode
    f.close()
    fname = zipFileLocation + 'zipcty7.txt'
    print(fname)
    f = open(fname, 'r+')
    for row in f:
        zipcode = row[0:5]
        if (zipcode != trailingzip):
            statecode = match_abbrev_code(states, row[23:25])
            if (statecode == None):
                continue
            countycode = row[25:28]
            fips = statecode + countycode
            personWriter.writerow([zipcode] + [fips])
            trailingzip = zipcode
    f.close()
    fname = zipFileLocation + 'zipcty8.txt'
    print(fname)
    f = open(fname, 'r+')
    for row in f:
        zipcode = row[0:5]
        if (zipcode != trailingzip):
            statecode = match_abbrev_code(states, row[23:25])
            if (statecode == None):
                continue
            countycode = row[25:28]
            fips = statecode + countycode
            personWriter.writerow([zipcode] + [fips])
            trailingzip = zipcode
    f.close()
    fname = zipFileLocation + 'zipcty9.txt'
    print(fname)
    f = open(fname, 'r+')
    for row in f:
        zipcode = row[0:5]
        if (zipcode != trailingzip):
            statecode = match_abbrev_code(states, row[23:25])
            if (statecode == None):
                continue
            countycode = row[25:28]
            fips = statecode + countycode
            personWriter.writerow([zipcode] + [fips])
            trailingzip = zipcode
    f.close()
    fname = zipFileLocation + 'zipcty10.txt'
    print(fname)
    f = open(fname, 'r+')
    for row in f:
        zipcode = row[0:5]
        if (zipcode != trailingzip):
            statecode = match_abbrev_code(states, row[23:25])
            if (statecode == None):
                continue
            countycode = row[25:28]
            fips = statecode + countycode
            personWriter.writerow([zipcode] + [fips])
            trailingzip = zipcode
    f.close()
    h.close()
    return []

#zips1 = read_zips()
#print(zips1)