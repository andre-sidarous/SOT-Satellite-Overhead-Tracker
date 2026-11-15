import requests

x = requests.get("https://celestrak.org/NORAD/elements/gp.php?CATNR=25544&FORMAT=JSON")
print(x.text, "A")