import sys
import json
from argparse import ArgumentParser
from utilities import utilities

if __name__ == "__main__":
    __last_date__ = utilities.data.today["date"]

    # Argument parsing setup
    parser = ArgumentParser()
    parser.add_argument('url', type=str, help='The source URL to be added.')
    parser.add_argument('--date', type=str, default=__last_date__, help='The date to which this source URL should be added. Defaults to the latest day in the dataset.')
    args = parser.parse_args()

    url = args.url
    date = args.date

    month = date[:7]
    data = utilities.data.data_for_month(month)
    day_data = [d for d in data if d["date"] == date][0]
    data_file = f"daily-data/{month}.json"

    if day_data["sources"] is None:
        day_data["sources"] = [url]
    else:
        day_data["sources"].append(url)
    utilities.save_json(data, data_file)