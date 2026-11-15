import requests
import json
import math
from sgp4.api import Satrec, WGS72, jday
from skyfield.api import EarthSatellite, load, wgs84
from datetime import datetime

# 1. Get the data from Celestrak
A = requests.get("https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=JSON")
print(A.text)
# x = requests.get("https://celestrak.org/NORAD/elements/gp.php?CATNR=25544&FORMAT=JSON")
# y = json.loads(x.text)[0]

# # 2. Define orbital parameters (converted to SGP4 units)
# epoch_str = y["EPOCH"] #Celestrak gives the date in ISO format
# dt = datetime.fromisoformat(epoch_str)
# seconds_with_fraction = dt.second + (dt.microsecond / 1_000_000) # Combine whole seconds and microseconds into a single float
# jd, fr = jday(
#     dt.year,     # 2026
#     dt.month,    # 11
#     dt.day,      # 15
#     dt.hour,     # 4
#     dt.minute,   # 56
#     seconds_with_fraction  # 48.710112
# )
# epoch_days_since_1949 = (jd + fr) - 2433281.5

# bstar = float(y["BSTAR"]) #Drag coefficient (1 / earth radii)
# ndot = float(y["MEAN_MOTION_DOT"]) #First derivative of mean motion (rad/min^2)
# nddot = float(y["MEAN_MOTION_DDOT"]) #Second derivative of mean motion (rad/min^3)
# eccentricity = float(y["ECCENTRICITY"]) #Unitless (0 to <1). Represents how close to a circle the orbit is.
# arg_of_pericenter = math.radians(float(y["ARG_OF_PERICENTER"])) #Must be in radians
# inclination = math.radians(float(y["INCLINATION"])) #Must be in radians
# mean_anomaly = math.radians(float(y["MEAN_ANOMALY"])) #Must be in radians
# raan = math.radians(float(y["RA_OF_ASC_NODE"])) #Right ascension of ascending node (radians)

# # Mean motion must be in radians per minute (not revs/day as Celestrak gives)
# revs_per_day = y["MEAN_MOTION"]
# mean_motion = revs_per_day * (2 * math.pi / 1440.0)

# # 2. Create the Satrec (SGP4 satellite record) object from the Celestrak numbers
# satrec = Satrec()
# satrec.sgp4init(
#     WGS72,                  # Gravity model
#     'i',                    # 'i' = improved mode, 'a' = old AFSPC mode
#     y["NORAD_CAT_ID"],      # The catalog number for the object
#     epoch_days_since_1949,  # Epoch: days since 1949 December 31 00:00 UT
#     bstar,
#     ndot,
#     nddot,
#     eccentricity,
#     arg_of_pericenter,
#     inclination,
#     mean_anomaly,
#     mean_motion,
#     raan
# )

# # 3. Wrap the Satrec in Skyfield and calculate ground coordinates
# ts = load.timescale()
# satellite = EarthSatellite.from_satrec(satrec, ts)#Makes the satrec object into a Skyfield object and gives it a timescale

# # Target time for ground location (can be the epoch itself or any future/past UTC time)
# t = ts.utc(dt.year, dt.month, dt.day, dt.hour, dt.minute, seconds_with_fraction)
# geocentric = satellite.at(t)#Converts the Satrec vectors into Skyfield position
# subpoint = wgs84.subpoint(geocentric)#Converts Skyfield position into latitude/longitude

# print(f"Latitude:  {subpoint.latitude.degrees:.4f}°")
# print(f"Longitude: {subpoint.longitude.degrees:.4f}°")
# print(f"Altitude:  {subpoint.elevation.km:.2f} km")