class activityPattern:
    def __init__(self, tripType, person):
        self.activityPattern = tripTypeToPattern(tripType)  
        self.activities = makeActivities(self.activityPattern, person)


'ActivityXYZ = [node type, sequence number, preceding, following, name, county, lat, lon, workindustry/otherindustry/schoolNA/homeNA]'
'Populate Attributes of Activities from Home, Work, or School, leaving Other trips unpopulated'
def makeActivities(activities, person):
    numActivities = activities[1]
    temp = [[], [], [], [], [], [], [], []]
    for k in range(0, numActivities + 1):
        temp[k] = [activities[2][k][0], k ] 
        type = activities[2][k][0]
        'Assign Name, Lat, Lon'
        if type == 'H':
            name = 'Home'
            lat = float(person[6])
            lon = float(person[7])
            indust = 'NA'
            county = person[0] + person[1]
        elif type == 'W':
            name = person[16]
            lat = float(person[27])
            lon = float(person[28])
            indust = (person[15])
            county = person[14]
        elif type == 'S':
            name = person[29]
            lat = float(person[31])
            lon = float(person[32])
            indust = 'NA'
            county = (person[30])
        elif type == 'O':
            name = 'NA'
            lat = 'NA'
            lon = 'NA'
            indust = 'NA'
            county = 'NA'
        try:
            preceding = activities[2][k-1][0]
        except IndexError:
            preceding = 'NA'
        try:
            proceeding = activities[2][k+1][0]
        except IndexError:
            proceeding = 'NA' 
        temp[k] = [activities[2][k][0], k, preceding, proceeding, name, county, lat, lon, indust]
    for k in range(numActivities + 1, 8):
        temp[k] = ['NA', 'NA', 'NA','NA', 'NA', 'NA','NA', 'NA', 'NA' ]
    return [temp[0], temp[1], temp[2], temp[3], temp[4], temp[5], temp[6]]

def tripTypeToPattern(tripType):
    '7 Possible Activities, which end and begin at home, which is included'
    'Activity = [type (H,W,S,O, N (fot null)), sequence number (0, 1,...,7)'
    activities = [tripType, [], [], [], [], [], [], [], []]
    if tripType == -5:
        activities = [tripType, 0, [['H', 0], ['N', 1], ['N', 2], ['N', 3], ['N', 4], ['N', 5], ['N', 6], ['N', 7]]]
    if tripType == 0:
        activities = [tripType, 0, [['H', 0], ['N', 1], ['N', 2], ['N', 3], ['N', 4], ['N', 5], ['N', 6], ['N', 7]]]
    elif tripType == 1:
        activities = [tripType, 2, [['H', 0], ['W', 1], ['H', 2], ['N', 3], ['N', 4], ['N', 5], ['N', 6], ['N', 7]]]
    elif tripType == 2:
        activities = [tripType, 2, [['H', 0], ['S', 1], ['H', 2], ['N', 3], ['N', 4], ['N', 5], ['N', 6], ['N', 7]]]
    elif tripType == 3:
        activities = [tripType, 2, [['H', 0], ['O', 1], ['H', 2], ['N', 3], ['N', 4], ['N', 5], ['N', 6], ['N', 7]]]
    elif tripType == 4:
        activities = [tripType, 3, [['H', 0], ['S', 1], ['W', 2], ['H', 3], ['N', 4], ['N', 5], ['N', 6], ['N', 7]]]
    elif tripType == 5:
        activities = [tripType, 3, [['H', 0], ['W', 1], ['S', 2], ['H', 3], ['N', 4], ['N', 5], ['N', 6], ['N', 7]]]
    elif tripType == 6:
        activities = [tripType, 3, [['H', 0], ['W', 1], ['O', 2], ['H', 3], ['N', 4], ['N', 5], ['N', 6], ['N', 7]]]
    elif tripType == 7:
        activities = [tripType, 3, [['H', 0], ['S', 1], ['O', 2], ['H', 3], ['N', 4], ['N', 5], ['N', 6], ['N', 7]]] 
    elif tripType == 8:
        activities = [tripType, 3, [['H', 0], ['O', 1], ['O', 2], ['H', 3], ['N', 4], ['N', 5], ['N', 6], ['N', 7]]] 
    elif tripType == 9:
        activities = [tripType, 4, [['H', 0], ['S', 1], ['W', 2], ['O', 3], ['H', 4], ['N', 5], ['N', 6], ['N', 7]]]
    elif tripType == 10:
        activities = [tripType, 4, [['H', 0], ['W', 1], ['S', 2], ['O', 3], ['H', 4], ['N', 5], ['N', 6], ['N', 7]]]
    elif tripType == 11:
        activities = [tripType, 4, [['H', 0], ['W', 1], ['H', 2], ['O', 3], ['H', 4], ['N', 5], ['N', 6], ['N', 7]]]
    elif tripType == 12:
        activities = [tripType, 4, [['H', 0], ['S', 1], ['H', 2], ['O', 3], ['H', 4], ['N', 5], ['N', 6], ['N', 7]]]
    elif tripType == 13:
        activities = [tripType, 4, [['H', 0], ['O', 1], ['H', 2], ['O', 3], ['H', 4], ['N', 5], ['N', 6], ['N', 7]]]
    elif tripType == 14:
        activities = [tripType, 4, [['H', 0], ['W', 1], ['O', 2], ['W', 3], ['H', 4], ['N', 5], ['N', 6], ['N', 7]]]
    elif tripType == 15:
        activities = [tripType, 5, [['H', 0], ['W', 1], ['O', 2], ['H', 3], ['O', 4], ['H', 5], ['N', 6], ['N', 7]]]
    elif tripType == 16:
        activities = [tripType, 5, [['H', 0], ['S', 1], ['O', 2], ['H', 3], ['O', 4], ['H', 5], ['N', 6], ['N', 7]]]
    elif tripType == 17:
        activities = [tripType, 5, [['H', 0], ['W', 1], ['H', 2], ['O', 3], ['O', 4], ['H', 5], ['N', 6], ['N', 7]]]
    elif tripType == 18:
        activities = [tripType, 5, [['H', 0], ['S', 1], ['H', 2], ['O', 3], ['O', 4], ['H', 5], ['N', 6], ['N', 7]]]
    elif tripType == 19:
        activities = [tripType, 7, [['H', 0], ['W', 1], ['O', 2], ['H', 3], ['O', 4], ['H', 5], ['O', 6], ['H', 7]]]
    elif tripType == 20:
        activities = [tripType, 7, [['H', 0], ['S', 1], ['O', 2], ['H', 3], ['O', 4], ['H', 5], ['O', 6], ['H', 7]]]
    return activities