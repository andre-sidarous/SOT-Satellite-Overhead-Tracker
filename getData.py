import requests
from datetime import datetime, UTC

"""
Gets fresh data if 2 hours have elapsed since the data was last updated.
"""

def getData(filename="data2"):
    filepath = f"{filename}.txt"
    
    # 1. Read the file in read mode 
    try:
        with open(filepath, "r") as f:
            lines = f.readlines()
            lastWrittenDate = datetime.fromisoformat(lines[1].strip())
            hoursPassed = (datetime.now(UTC) - lastWrittenDate).total_seconds() / 3600
    except (FileNotFoundError, IndexError):
        # If the file doesn't exist, force the writing
        hoursPassed = 2

    # 2. If it's been 2+ hours (Celestrak GP data update frequency) since the last write, then get new data. Otherwise do nothing (it'll break Celestrak's usage limits)
    if hoursPassed >= 2:
        A = requests.get("https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=JSON")
        #Only overwrite it if the data fetch was successful
        if A.status_code == 200:
            with open(filepath, "w") as f:
                f.writelines([f"{A.text}", f"{datetime.now(UTC).isoformat()}\n"])