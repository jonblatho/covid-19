import sys
import os
import json
sys.path.append(os.path.realpath('.'))
from process import daily_data

try:
    url = sys.argv[1]
except IndexError:
    print("No URL was provided. Exiting.")
    exit()

last_date = daily_data[-1]["date"]
data_file = "daily-data/" + last_date[:7] + ".json"

with open(data_file, 'r+') as f:
    days = json.load(f)
    days[-1]["sources"] = [url]
    f.truncate()
    f.write(json.dumps(days, separators=(',', ':')))