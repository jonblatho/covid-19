import json
import os
import sys
sys.path.append(os.path.realpath('.'))
# from process import daily_data, index_for_date, data_for_month
from utilities import utilities
from argparse import ArgumentParser

# Argument parsing setup
parser = ArgumentParser()
parser.add_argument('-c', '--count', type=int, dest='count', required=True, help='The test count to add into the data at the given date.')
parser.add_argument('-d', '--date', type=str, dest='date', required=False, default=utilities.data.today["date"], help='The date to which the test count should be added. If not given, defaults to the latest available date.')
parser.add_argument('-u', '--url', type=str, dest='url', required=False, help='A source URL to append for this test count. Optional but recommended.')
args = parser.parse_args()

count = args.count
date = args.date
url = args.url

data = utilities.data.cumulative_data(date)

# Find the most recent day with a confirmed test count
most_recent_confirmed = [d for d in data[:-1] if not d["estimates"]["tests"]][-1]["date"]
print(most_recent_confirmed)
data_range = utilities.data.data_for_date_range(most_recent_confirmed, date)

for i, day in enumerate(data_range, start=1):
    print(day)
    
i0 = index_for_date(most_recent_confirmed)

# Create range of indices over which we'll be applying estimates
index_range = range(i0+1, date_index+1)
index_start = index_range[0]
index_end = index_range[-1]+1
last_test_count = data[i0]["tests"]
delta = (count - last_test_count) / len(index_range)

# Apply estimates
for i, index in enumerate(index_range, start=1):
    data[index]["tests"] = last_test_count + int(round(i*delta,0))

# For the last day, remove the estimate flag and add a URL if provided
data[date_index]["estimates"]["tests"] = False
if url is not None and daily_data[date_index]["sources"] is not None:
    data[date_index]["sources"].append(url)
elif url is not None:
    data[date_index]["sources"] = [url]

for day in daily_data:
    if "other" in day["new_cases"]:
        day["new_cases"].pop("other", None)

# Split modified data by month and save
months = utilities.unique([d["date"][:7] for d in data[index_start:index_end]])
for month in months:
    data_file = f"daily-data/{month}.json"

    # with open(data_file, 'r+') as f:
    #     f.seek(0)
    #     f.write(json.dumps(data_for_month(month), separators=(',', ':')))
    #     print(f'Saved updated data to {data_file}')
    #     f.truncate()