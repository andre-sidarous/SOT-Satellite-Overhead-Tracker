import requests
import json

A = requests.get("https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=JSON")
print(a.text)