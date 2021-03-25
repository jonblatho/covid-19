import json
from calendar import monthrange
from datetime import date
from glob import glob

cities = ["Howell County", "West Plains", "Willow Springs", "Mountain View", "Other"]
city_slugs = ["west_plains", "willow_springs", "mountain_view", "other"]
city_slugs_county = ["county", "west_plains", "willow_springs", "mountain_view", "other"]

# Load in daily data
daily_data = []
month_files = glob('daily-data/*.json')
for month_path in month_files:
    with open(month_path, 'r') as month_file:
        month_data = json.load(month_file)
        daily_data.extend(month_data)
    month_file.close()
# Sort daily data by date
daily_data = sorted(daily_data, key = lambda i : i['date'])

# Outputs JSON for the given dictionary or list to the given path.
def save_json(x, path):
    with open(path, 'w+') as output_file:
        output_file.write(json.dumps(x))
        print('Saved '+path)

# Sets "today" to the last day for which there is data
today = daily_data[-1]["date"]
week_ago = daily_data[-8]["date"]

# Returns (year, month, date) as strings for a given YYYY-MM-DD
# formatted date.
def date_components(d):
    return (d[:4], d[5:7], d[8:])

# Returns (year, month, date) as integers for a given YYYY-MM-DD
# formatted date.
def date_components_int(d):
    yyyy, mm, dd = date_components(d)
    # Remove leading zeroes from month and day
    if mm[0] == '0':
        mm = mm[1]
    if dd[0] == '0':
        dd = dd[1]
    return tuple(int(n) for n in (yyyy, mm, dd))

# Returns the expected index for a given date.
def index_for_date(d):
    start = date.fromisoformat('2020-04-01')
    end = date.fromisoformat(d)
    return (end - start).days

# Returns the number of days in the month of the given date.
def days_in_month(d):
    y, m, _ = date_components_int(d)
    return monthrange(y, m)[1]

# Generate a list of months
months = []
for date_str in [_["date"] for _ in daily_data]:
    if date_str[0:7] not in months:
        months.append(date_str[:7])

# Returns the start and end indices for the given month (YYYY-MM) 
# as a tuple.
def data_for_month(m):
    month_first_day = m+'-01'
    start_index = index_for_date(month_first_day)
    offset = days_in_month(month_first_day)
    return daily_data[start_index:start_index+offset]
    
# Returns data for the current month up to today.
def mtd_data():
    return data_for_month(today[:7])

# Returns data for the current year up to today.
def ytd_data():
    y = date_components_int(today)[0]
    start_index = index_for_date(str(y)+'-01-01')
    return daily_data[start_index:]

# Returns data for the n days ended on the current date, if 
# possible.
def data_days_ended(n, d):
    end_index = index_for_date(d)
    return daily_data[end_index-n+1:end_index+1]

# Returns data for the n days ended on the most recent date, 
# if possible.
def data_past_n_days(n):
    return daily_data[-n:]

# Returns a list of summed new cases for the county and by town 
# for the given data slice.
def case_sum_list(d):
    cases = [sum([sum(day["new_cases"].values()) for day in d])]
    for slug in city_slugs:
        cases.append(sum([day["new_cases"][slug] for day in d]))
    return cases

# Calculates estimated active cases by town
def active_cases_by_town():
    output = []
    if cases_past_week[0] > 0:
        for v in cases_past_week:
            output.append(round(v/cases_past_week[0]*daily_data[-1]["active_cases"], 2))
    else:
        return [0, 0, 0, 0, 0]
    return output[1:]

# Calculates (if possible) the cases added by town over the n-day
# period ended on date d. Default is 7 days.
def cases_added(d, n=7):
    end_index = min(index_for_date(d), index_for_date(today))
    start_index = end_index-n+1
    estimated = bool(daily_data[start_index]["estimates"]["cases"] or daily_data[end_index]["estimates"]["cases"])
    return {'value': sum([sum(day["new_cases"].values()) for day in daily_data[start_index:end_index+1]]), 'estimate': estimated}

# Calculates (if possible) the tests added over the n-day period
# ended on date d. Default is 14 days.
def tests_added(d, n=14):
    end_index = min(index_for_date(d), index_for_date(today))
    start_index = end_index-n
    if daily_data[start_index]["tests"] is not None and daily_data[end_index]["tests"] is not None:
        estimated = bool(daily_data[start_index]["estimates"]["tests"] or daily_data[end_index]["estimates"]["tests"])
        return {'value': daily_data[end_index]["tests"] - daily_data[start_index]["tests"], 'estimate': estimated}
    return None

# Calculates (if possible) the n-day positivity rate for the period
# ended on date d. Default is 14 days.
def positivity_rate(d, n=14):
    cases = case_sum_list(data_days_ended(n, d))[0]
    tests = tests_added(d, n)
    if tests is not None:
        end_index = min(index_for_date(d), index_for_date(today))
        start_index = end_index-n
        estimated = bool(daily_data[start_index]["estimates"]["tests"] or daily_data[end_index]["estimates"]["tests"]\
            or daily_data[start_index+1]["estimates"]["cases"] or daily_data[end_index]["estimates"]["cases"])
        return {'value': float(round(cases/tests["value"]*100, 2)), 'estimate': estimated}
    return None

# Calculates the categorical risk level for the given date.
def risk_level(d):
    cases = case_sum_list(data_days_ended(7, d))[0]
    if cases is not None:
        average_daily_cases_7d_100k = cases/7*100000/40400
        if average_daily_cases_7d_100k < 1:
            return "low"
        if average_daily_cases_7d_100k < 10:
            return "medium"
        if average_daily_cases_7d_100k < 25:
            return "high"
        if average_daily_cases_7d_100k < 75:
            return "critical"
        return "extreme"
    return None

if __name__ == "__main__":
    # Calculate date-relative totals
    cases_new = case_sum_list(data_past_n_days(1))
    cases_past_week = case_sum_list(data_past_n_days(7))
    cases_mtd = case_sum_list(mtd_data())
    cases_ytd = case_sum_list(ytd_data())
    cases_cumulative = case_sum_list(daily_data)
    # Save the JSON file
    relative = [
        {'label': 'Today', 'totals': cases_new},
        {'label': 'Past Week', 'totals': cases_past_week},
        {'label': 'MTD', 'totals': cases_mtd},
        {'label': 'YTD', 'totals': cases_ytd},
        {'label': 'All', 'totals': cases_cumulative}
    ]
    save_json(relative, 'data/relative.json')

    # Calculate monthly totals
    monthly_totals = [{'month': month, 'totals': case_sum_list(data_for_month(month))} for month in months]
    save_json(monthly_totals, 'data/monthly.json')

    # Calculate active cases by town
    active_by_town = [{'town': cities[i+1], 'active': active_cases_by_town()[i]} for i, _ in enumerate(active_cases_by_town())]
    save_json(active_by_town, 'data/active_town.json')

    # Calculate summary data
    new_cases_7d_change_est = bool(cases_added(today)["estimate"] or cases_added(week_ago)["estimate"])
    new_tests_7d_change_est = bool(tests_added(today, n=7)["estimate"] or tests_added(week_ago, n=7)["estimate"])
    positivity_rate_2w_change_est = bool(positivity_rate(today)["estimate"] or positivity_rate(week_ago)["estimate"])
    summary = {
        'last_updated': daily_data[-1]["date"],
        'new_cases_7d': cases_added(today),
        'new_cases_change': {'value': cases_added(today)["value"] - cases_added(week_ago)["value"], 'estimate': new_cases_7d_change_est},
        'active_cases': {'value': daily_data[-1]["active_cases"], 'estimate': daily_data[-1]["estimates"]["active"]},
        'active_cases_change': {'value': daily_data[-1]["active_cases"] - daily_data[-8]["active_cases"], 'estimate': daily_data[-8]["estimates"]["active"]},
        'deaths': {'value': daily_data[-1]["deaths"], 'estimate': daily_data[-1]["estimates"]["deaths"]},
        'deaths_change': {'value': daily_data[-1]["deaths"] - daily_data[-8]["deaths"], 'estimate': daily_data[-8]["estimates"]["deaths"]},
        'positivity_rate_2w': positivity_rate(today),
        'positivity_rate_2w_change': {'value': positivity_rate(today)["value"] - positivity_rate(week_ago)["value"], 'estimate': positivity_rate_2w_change_est},
        'new_tests_7d': tests_added(today, n=7),
        'new_tests_7d_change': {'value': tests_added(today, n=7)["value"] - tests_added(week_ago, n=7)["value"], 'estimate': new_tests_7d_change_est}
    }
    save_json(summary, 'data/summary.json')

    # Calculate table data
    table_data = []
    for i, day in enumerate(daily_data):
        table_day = dict()
        # Transfer date key
        table_day["date"] = day["date"]
        # Calculate total and new cases
        table_day["total_cases"] = dict(zip(city_slugs_county, case_sum_list(daily_data[:i+1])))
        table_day["new_cases"] = dict(zip(city_slugs_county, case_sum_list([day])))
        # Transfer active cases, hospitalizations, deaths, source links, and estimates
        table_day["active_cases"] = day["active_cases"]
        table_day["hospitalizations"] = day["hospitalizations"]
        table_day["deaths"] = day["deaths"]
        table_day["estimates"] = day["estimates"]
        # Where possible, add in total/new tests
        table_day["tests"] = dict()
        if day["tests"] is not None:
            table_day["tests"]["total"] = day["tests"]
            if daily_data[i-1]["tests"] is not None:
                table_day["tests"]["new"] = day["tests"] - daily_data[i-1]["tests"]
        # Where possible, calculate the 14D positivity rate and risk level
        if positivity_rate(day["date"]) is not None:
            table_day["positivity_rate"] = positivity_rate(day["date"])
        if risk_level(day["date"]) is not None:
            table_day["risk_level"] = risk_level(day["date"])
        # Transfer sources key
        if day["sources"] is not None:
            table_day["sources"] = [{'number': j, 'url': source} for j, source in enumerate(day["sources"], start=1)]
        else:
            table_day["sources"] = None

        table_data.append(table_day)
    save_json(table_data, 'data/daily.json')

    # Calculate chart data
    chart_data = []
    for i, day in enumerate(daily_data):
        chart_day = dict()
        # Transfer date key
        chart_day["date"] = day["date"]
        # Calculate total and new cases
        chart_day["total_cases"] = dict(zip(city_slugs_county, case_sum_list(daily_data[:i+1])))
        chart_day["new_cases"] = dict(zip(city_slugs_county, case_sum_list([day])))
        # Calculate 7D average new cases
        if i >= 7:
            chart_day["average_daily_cases_7d"] = round(sum([sum(day_data["new_cases"].values()) for day_data in daily_data[i-6:i+1]])/7, 1)
        # Transfer active cases
        chart_day["active_cases"] = day["active_cases"]
        # Calculate 7D average active cases
        chart_day["average_active_cases_7d"] = round(sum([day_data["active_cases"] for day_data in daily_data[i-6:i+1]])/7, 1)
        # Where possible, add in total/new tests
        chart_day["tests"] = dict()
        if day["tests"] is not None:
            chart_day["tests"]["total"] = day["tests"]
            if daily_data[i-1]["tests"] is not None:
                chart_day["tests"]["new"] = day["tests"] - daily_data[i-1]["tests"]
                if daily_data[i-15]["tests"] is not None:
                    chart_day["tests"]["average_14d"] = round((daily_data[i]["tests"] - daily_data[i-15]["tests"])/14, 1)
        # Where possible, calculate the 14D positivity rate and risk level
        if positivity_rate(day["date"]) is not None:
            chart_day["positivity_rate"] = positivity_rate(day["date"])["value"]
        chart_data.append(chart_day)
    save_json(chart_data, 'assets/js/chart-data.json')