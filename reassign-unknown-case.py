import sys
import json
from argparse import ArgumentParser
from utilities import utilities

if __name__ == "__main__":
    __last_date__ = utilities.data.today["date"]

    # Argument parsing setup
    parser = ArgumentParser()
    parser.add_argument('town', type=str, help='The town to which the unknown case should be reassigned.')
    parser.add_argument('-n', '--number', type=int, default=1, help='The number of cases to reassign. Defaults to 1.')
    parser.add_argument('-d', '--date', type=str, default=__last_date__, help='The date to which this source URL should be added. Defaults to the latest day in the dataset.')
    args = parser.parse_args()

    town = args.town
    number = args.number
    date = args.date

    month = date[:7]
    data = utilities.data.data_for_month(month)
    try:
        day_data = [d for d in data if d["date"] == date][0]
    except:
        print(f'{date} is not in the dataset.')
        exit(95)
    data_file = f"daily-data/{month}.json"

    if town not in utilities.geo.towns and town != 'unknown':
        print('Invalid town argument provided. Valid towns:')
        for t in [t for t in utilities.geo.towns if t != 'unknown']:
            print(' * '+t)
        exit(96)
    elif day_data["new_cases"]["unknown"] == 0:
        print(f'There are no unknown cases for {date}.')
        exit(97)
    elif number < 1 or number > day_data["new_cases"]["unknown"]:
        print(f'Invalid case number argument provided; must be at least 1 and less than or equal to the number of unknown cases for {date} ({day_data["new_cases"]["unknown"]}).')
        exit(98)

    day_data["new_cases"]["unknown"] -= number
    day_data["new_cases"][town] += number
    
    utilities.save_json(data, data_file)