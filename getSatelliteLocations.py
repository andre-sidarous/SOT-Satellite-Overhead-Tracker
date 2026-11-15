import requests
import json
import numpy as np
from getLatitudeLongitude import getLatitudeLongitude
from getData import getData

##FOR A COORD WITH MULTIPLE SATELLITES: (0.0,46.2)
"""
Dictionary format: (Latitude, Longitude):[(Name1,Elevation1),(Name2,Elevation2)...]

Returns a dictionary (in the format above), that contains all satellites at a specific latitude and longitude
"""
def getSatelliteLocations(filename="data2"):
    satelliteDict = {}

    getData() #Make sure you get fresh data (if necessary)
    with open(f"{filename}.txt") as f:
        y = json.loads(f.readline())

        for i in range(len(y)):
            name = y[i]["OBJECT_NAME"]
            #Get the NumPy floats and convert them to Python floats
            latitude, longitude, elevation = getLatitudeLongitude(y[i])

            #Negative 0 results can split the same coord in 2
            if latitude == -0:
                latitude = 0
            elif longitude == -0:
                longitude = 0

            if (latitude, longitude) in satelliteDict:
                satelliteList = satelliteDict.get((latitude, longitude))
                satelliteList.append((name, elevation))
                satelliteDict[(latitude, longitude)] = satelliteList
            else:
                satelliteDict[(latitude, longitude)] = [(name, elevation)]
        
        f.close()
    
    return satelliteDict