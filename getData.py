import requests
import json

A = requests.get("https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=JSON")

with open("data2.txt", 'w') as f:
    f.write(A.text)