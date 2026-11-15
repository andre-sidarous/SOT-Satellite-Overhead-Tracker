import requests
import json
import numpy as np
from getLatitudeLongitude import getLatitudeLongitude

##FOR A COORD WITH MULTIPLE SATELLITES: (0.0,46.2)
"""
Dictionary format: (Latitude, Longitude):[(Name1,Elevation1),(Name2,Elevation2)...]

Returns a dictionary (in the format above), that contains all satellites at a specific latitude and longitude
"""

def getSatelliteLocations(filename="data2"):
    satelliteDict = {}

    with open(f"{filename}.txt") as f:
        y = json.loads(f.read())

        for i in range(len(y)-1):
            name = y[i]["OBJECT_NAME"]
            #Get the NumPy floats and convert them to Python floats
            latitudeNp, longitudeNp, elevationNp = getLatitudeLongitude(y[i])
            latitude = latitudeNp.item()
            longitude = longitudeNp.item()
            elevation = elevationNp.item()

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