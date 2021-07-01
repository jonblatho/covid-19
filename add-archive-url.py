import sys
import os
import json
from utilities import utilities

try:
    url = sys.argv[1]
except IndexError:
    print("No URL was provided. Exiting.")
    exit()

last_date = utilities.data.all[-1]["date"]
data_file = "daily-data/" + last_date[:7] + ".json"

with open(data_file, 'r+') as f:
    days = json.load(f)
    days[-1]["sources"] = [url]
    f.seek(0)
    f.write(json.dumps(days, separators=(',', ':')))
    f.truncate()