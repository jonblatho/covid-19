import sys, os
import json
import csv
from argparse import ArgumentParser
from utilities import date, utilities

# Argument parsing setup
parser = ArgumentParser()
parser.add_argument('file', type=str, help='The vaccination CSV data file to process.')
args = parser.parse_args()

with open(args.file, 'r', encoding='utf-16') as csv_file:
    dates = [d["date"] for d in utilities.data.all]

    def __reformatted_date__(d: str):
        components = [int(component) for component in d.split('/')]
        for k, component in enumerate(components):
            if component < 10:
                components[k] = f"0{component}"
            else:
                components[k] = str(component)
        return f"{components[2]}-{components[0]}-{components[1]}"

    reader = csv.reader(csv_file, delimiter='\t')
    # Filter to Howell County rows only
    howell_rows = [row for row in reader if row[1] == "HOWELL"]
    for row in howell_rows:
        # Reformat the date to our expected YYYY-MM-DD format
        row[0] = __reformatted_date__(row[0])
    # Reorder rows list by date in ascending order
    rows = sorted(howell_rows, key = lambda i : i[0])
    # Set up cumulative total variable for initiated/completed vaccinations
    cumulative_total = 0
    for day in utilities.data.all:
        # Filter to rows for the current date and remove serology tests and positive case information
        date_rows = [row for row in rows if row[0] == day["date"] and row[2] != 'Serology Tests' and 'Cases' not in row[2]]
        # Correct formatting for zero values
        for row in date_rows:
            if row[3] == '':
                row[3] = '0'
        value = sum([int(v[3].replace(',','')) for v in date_rows])
        cumulative_total += value
        # Store data
        day["tests"] = cumulative_total
        day["estimates"]["tests"] = False

# Save monthly data
months = utilities.unique([d["date"][:7] for d in utilities.data.all])
for month in months:
    utilities.save_json(utilities.data.data_for_month(month), f'daily-data/{month}.json')