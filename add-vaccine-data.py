import sys, os
import json
import csv
from argparse import ArgumentParser
from utilities import utilities

# Argument parsing setup
parser = ArgumentParser()
parser.add_argument('path', type=str, help='The path to the vaccination CSV data file to process.')
parser.add_argument('--type', type=str, choices=['doses', 'initiated', 'completed'], help='The vaccination data file type. This argument is optional if the path is provided and the data file names are present and unchanged from what was received from the DHSS server.')
parser.add_argument('--quiet', action='store_true', help='Suppress non-error output.')
args = parser.parse_args()

# Pull arguments from arg parser
data_path = args.path
data_type = args.type

# If type isn't provided, attempt to guess the type
if data_type is None and data_path is not None:
    if "doses" in data_path.lower():
        data_type = "doses"
    elif "initiated" in data_path.lower():
        data_type = "initiated"
    elif "completed" in data_path.lower():
        data_type = "completed"
    else:
        print("Unable to guess the type of vaccine data file provided.")
        print('Please retry and explicitly provide the type as "--type doses", "--type initiated", or "--type completed" following the file path. Exiting.')
        exit(1)

with open(data_path, 'r', encoding='utf-8') as csv_file:
    dates = [d["date"] for d in utilities.data.all]

    def __reformatted_date__(d: str):
        components = [int(component) for component in d.split('/')]
        for k, component in enumerate(components):
            if component < 10:
                components[k] = f"0{component}"
            else:
                components[k] = str(component)
        return f"{components[2]}-{components[0]}-{components[1]}"

    reader = csv.reader(csv_file, delimiter=',')
    # Filter to Howell County rows only
    howell_rows = [row for row in reader if row[1] == "Howell"]
    for row in howell_rows:
        # Reformat the date to our expected YYYY-MM-DD format
        row[0] = __reformatted_date__(row[0])
    # Reorder rows list by date in ascending order
    rows = sorted(howell_rows, key = lambda i : i[0])
    # Set up cumulative total variable for initiated/completed vaccinations
    cumulative_total = 0
    for day in utilities.data.all:
        if utilities.date.date_is_before(day["date"], '2020-12-15'):
            # No doses were administered before 2020-12-15
            if not args.quiet:
                print(day["date"], "is before 2020-12-14. Skipping.")
            day["vaccinations"] = None
            continue
        # Filter to rows for the current date
        date_rows = [row for row in rows if row[0] == day["date"]]
        if data_type == 'doses':
            value_index = 2
        elif data_type == 'initiated' or data_type =='completed':
            value_index = 3
        # Sum the filtered values 
        value = sum([int(v[value_index].replace(',','')) for v in date_rows])
        cumulative_total += value
        # Store data
        if "vaccinations" not in day or day["vaccinations"] is None:
            day["vaccinations"] = {"doses": None, "initiated": None, "completed": None}
        day["vaccinations"][data_type] = value

# Save monthly data
months = utilities.unique([d["date"][:7] for d in utilities.data.all])
for month in months:
    utilities.save_json(utilities.data.data_for_month(month), f'daily-data/{month}.json', quiet=args.quiet)