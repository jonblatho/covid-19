import json
import os
import sys
sys.path.append(os.path.realpath('.'))
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
data_range = utilities.data.data_for_date_range(most_recent_confirmed, date)
last_test_count = data_range[0]["tests"]
delta = (count - last_test_count) / (len(data_range)-1) # Estimated daily increase in tests

if count < last_test_count:
    print('Input test count is lower than the most recent confirmed test count. Exiting.')
    exit(1)

for i, day in enumerate(data_range, start=0):
    # Apply estimates
    day["tests"] = int(round(last_test_count+i*delta, 0))

# For the last day, remove the estimate flag and add a URL if provided
data_range[-1]["estimates"]["tests"] = False
if url is not None and data_range[-1]["sources"] is not None:
    data_range[-1]["sources"].append(url)
elif url is not None:
    data_range[-1]["sources"] = [url]

# Split modified data by month and save
months = utilities.unique([d["date"][:7] for d in data_range[1:]])
for month in months:
    data_file = f"daily-data/{month}.json"
    month_data = utilities.data.data_for_month(month)

    with open(data_file, 'w+') as f:
        f.seek(0)
        f.write(json.dumps(month_data, separators=(',', ':')))
        print(f'Saved updated data to {data_file}')
        f.truncate()