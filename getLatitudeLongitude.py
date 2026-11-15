import math
import json
import numpy as np
from sgp4.api import Satrec, WGS72, jday
from skyfield.api import EarthSatellite, load, wgs84
from datetime import datetime

"""
Example Celestrak output (this is the ISS):

[
  {
    "OBJECT_NAME": "ISS (ZARYA)",
    "OBJECT_ID": "1998-067A",
    "EPOCH": "2026-11-15T04:56:48.710112",
    "MEAN_MOTION": 15.49388394,
    "ECCENTRICITY": 0.00073773,
    "INCLINATION": 51.6322,
    "RA_OF_ASC_NODE": 272.7605,
    "ARG_OF_PERICENTER": 27.6155,
    "MEAN_ANOMALY": 332.5225,
    "EPHEMERIS_TYPE": 0,
    "CLASSIFICATION_TYPE": "U",
    "NORAD_CAT_ID": 25544,
    "ELEMENT_SET_NO": 999,
    "REV_AT_EPOCH": 59516,
    "BSTAR": 0.00019362061,
    "MEAN_MOTION_DOT": 0.00010382,
    "MEAN_MOTION_DDOT": 0
  }
]
"""

"""
Returns a latitude and longitude of an object, rounded to 1 decimal place, given the Celestrak JSON
"""
def getLatitudeLongitude(celestrakJSON):
    # 1. Define orbital parameters (converted to SGP4 units)
    epoch_str = celestrakJSON["EPOCH"] #Celestrak gives the date in ISO format
    dt = datetime.fromisoformat(epoch_str)
    seconds_with_fraction = dt.second + (dt.microsecond / 1_000_000) # Combine whole seconds and microseconds into a single float
    jd, fr = jday(
        dt.year,     # 2026
        dt.month,    # 11
        dt.day,      # 15
        dt.hour,     # 4
        dt.minute,   # 56
        seconds_with_fraction  # 48.710112
    )
    epoch_days_since_1949 = (jd + fr) - 2433281.5

    bstar = float(celestrakJSON["BSTAR"]) #Drag coefficient (1 / earth radii)
    ndot = float(celestrakJSON["MEAN_MOTION_DOT"]) #First derivative of mean motion (rad/min^2)
    nddot = float(celestrakJSON["MEAN_MOTION_DDOT"]) #Second derivative of mean motion (rad/min^3)
    eccentricity = float(celestrakJSON["ECCENTRICITY"]) #Unitless (0 to <1). Represents how close to a circle the orbit is.
    arg_of_pericenter = math.radians(float(celestrakJSON["ARG_OF_PERICENTER"])) #Must be in radians
    inclination = math.radians(float(celestrakJSON["INCLINATION"])) #Must be in radians
    mean_anomaly = math.radians(float(celestrakJSON["MEAN_ANOMALY"])) #Must be in radians
    raan = math.radians(float(celestrakJSON["RA_OF_ASC_NODE"])) #Right ascension of ascending node (radians)
    # Mean motion must be in radians per minute (not revs/day as Celestrak gives)
    revs_per_day = celestrakJSON["MEAN_MOTION"]
    mean_motion = revs_per_day * (2 * math.pi / 1440.0)

    # 2. Create the Satrec (SGP4 satellite record) object from the Celestrak numbers
    satrec = Satrec()
    satrec.sgp4init(
        WGS72,                  # Gravity model
        'i',                    # 'i' = improved mode, 'a' = old AFSPC mode
        celestrakJSON["NORAD_CAT_ID"],      # The catalog number for the object
        epoch_days_since_1949,  # Epoch: days since 1949 December 31 00:00 UT
        bstar,
        ndot,
        nddot,
        eccentricity,
        arg_of_pericenter,
        inclination,
        mean_anomaly,
        mean_motion,
        raan
    )

    # 3. Wrap the Satrec in Skyfield and calculate ground coordinates
    ts = load.timescale()
    satellite = EarthSatellite.from_satrec(satrec, ts)#Makes the satrec object into a Skyfield object and gives it a timescale
    # Target time for ground location (can be the epoch itself or any future/past UTC time)
    t = ts.utc(dt.year, dt.month, dt.day, dt.hour, dt.minute, seconds_with_fraction)
    geocentric = satellite.at(t)#Converts the Satrec vectors into Skyfield position
    subpoint = wgs84.subpoint(geocentric)#Converts Skyfield position into latitude/longitude

    return np.round(subpoint.latitude.degrees, decimals=1).item(), np.round(subpoint.longitude.degrees, decimals=1).item(), np.round(subpoint.elevation.km, decimals=1).item()