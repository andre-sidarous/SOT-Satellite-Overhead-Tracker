def seeIfCollision(latitude: float, latitudeVariance:float, longitude:float, longitudeVariance:float, satelliteDict: dict, maxElevation:float):
    # 1. Create the list of all valid coordinates given the variances provided
    coordinateList = []
    latitudeList = []
    longitudeList = []

    latVar = -latitudeVariance
    while latVar <= latitudeVariance:
        latitudeList.append(round(latitude+latVar,1))
        latVar += 0.1
    longVar = -longitudeVariance
    while longVar <= longitudeVariance:
        longitudeList.append(round(longitude+longVar,1))
        longVar += 0.1

    for i in range(len(latitudeList)):
        coordinateList.append((latitudeList[i], longitudeList[i]))

    # 2. Loop through that list and see if there's any matching key in the satelliteDict (if not then ignore it, if so, then add each one's name to the master list)
    satellitesToCollide = []
    for i in coordinateList:
        if i in satelliteDict:
            satellitesFound = satelliteDict.get(i)
            for i in range(0, len(satellitesFound)):
                if maxElevation >= satellitesFound[i][1]:
                    satellitesToCollide.append(satellitesFound[i][0])

    # 3. Return the master list
    return satellitesToCollide