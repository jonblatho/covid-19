from datetime import date, timedelta
from calendar import monthrange

# Returns the date d advanced by n days.
def _date_advanced_by_(d, n_days):
    start_date = date.fromisoformat(d)
    end_date = start_date + timedelta(days=n_days)
    return end_date.strftime("%Y-%m-%d")

# Whether the first given date is before the second given date.
def _date_is_before_(d, compare):
    first_date = date.fromisoformat(d)
    second_date = date.fromisoformat(compare)
    return bool(first_date < second_date)

# Returns (year, month, date) as strings for a given YYYY-MM-DD
# formatted date.
def _date_components_(d):
    return (d[:4], d[5:7], d[8:])

# Returns (year, month, date) as integers for a given YYYY-MM-DD
# formatted date.
def _date_components_int_(d):
    yyyy, mm, dd = _date_components_(d)
    # Remove leading zeroes from month and day
    if mm[0] == '0':
        mm = mm[1]
    if dd[0] == '0':
        dd = dd[1]
    return tuple(int(n) for n in (yyyy, mm, dd))

# Returns the number of days in the month of the given date.
def _days_in_month_(d):
    y, m, _ = _date_components_int_(d)
    return monthrange(y, m)[1]

# Returns the expected index for a given date.
def _index_for_date_(d):
    start = date.fromisoformat('2020-04-01')
    end = date.fromisoformat(d)
    return (end - start).days