from calendar import monthrange
from datetime import date, timedelta
from glob import glob
import json
from . import utilities

# Load in daily data
__daily_data__ = []
__month_files__ = glob('daily-data/*.json')
for month_path in __month_files__:
    with open(month_path, 'r') as month_file:
        month_data = json.load(month_file)
        __daily_data__.extend(month_data)
    month_file.close()

# All daily data in the dataset, sorted by date in ascending order.
all = sorted(__daily_data__, key = lambda i : i['date'])


# Returns data for the specified date.
def data_for_date(date):
    index = utilities.date._index_for_date_(date)
    if index >= 0:
        return all[index]
    else:
        return None

# Data for the most recent day available.
today = data_for_date(all[-1]["date"])

# Data for the day one week before the most recent day available.
def week_ago(d, inclusive=False):
    if inclusive:
        offset = -6
    else:
        offset = -7
    return data_for_date(utilities.date._date_advanced_by_(d, offset))

# Returns data for the specified date range.
def data_for_date_range(start_date, end_date):
    start_index = max(0, utilities.date._index_for_date_(start_date))
    end_index = utilities.date._index_for_date_(end_date)
    return all[start_index:end_index+1]

# Returns data from the beginning of the dataset to the given date range.
def cumulative_data(end_date=today["date"]):
    return data_for_date_range('2020-04-01', end_date)

# Returns year-to-date data for the given end date.
def ytd_data(end_date=today["date"]):
    year = end_date[:4]
    start_date = f'{year}-01-01'
    return data_for_date_range(start_date, end_date)

# Returns the data for the given month, through the given end date.
def data_for_month(month, end_date=today["date"]):
    if month == end_date[:7]:
        start_date = f'{month}-01'
        return data_for_date_range(start_date, end_date)
    else:
        month_date = f'{month}-01'
        return data_for_month(month, f'{month}-{utilities.date._days_in_month_(month_date)}')

# Returns month-to-date data for the given end date.
def mtd_data(end_date=today["date"]):
    month = end_date[:7]
    start_date = f'{month}-01'
    return data_for_date_range(start_date, end_date)

# Returns data for the n days ended on the given end date.
def data_for_days_ended(n, end_date=today["date"]):
    start_date = utilities.date._date_advanced_by_(end_date, -1*(n-1))
    return data_for_date_range(start_date, end_date)