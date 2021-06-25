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

# Calculate "other" new cases by summing smaller towns' new cases.
for day in daily_data:
    day["new_cases"]["total"] = sum(day["new_cases"].values())
    day["new_cases"]["other"] = day["new_cases"]["total"] - day["new_cases"]["west_plains"] - day["new_cases"]["willow_springs"] - day["new_cases"]["mountain_view"]

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
def months_list(d):
    months = []
    end_index = index_for_date(d)+1
    for date_str in [_["date"] for _ in daily_data[:end_index]]:
        if date_str[0:7] not in months:
            months.append(date_str[:7])
    return months

# Returns the start and end indices for the given month (YYYY-MM) 
# as a tuple.
def data_for_month(m, d=today):
    month_first_day = m+'-01'
    last_day = m+'-'+str(days_in_month(month_first_day))
    start_index = index_for_date(month_first_day)
    end_index = min(index_for_date(d), index_for_date(last_day))
    return daily_data[start_index:end_index+1]
    
# Returns data for the current month up to today.
def mtd_data(d=today):
    return data_for_month(d[:7])

# Returns data for the current year up to today.
def ytd_data(d=today):
    start_index = max(0, index_for_date(d[:4]+'-01-01'))
    end_index = index_for_date(d)
    return daily_data[start_index:end_index+1]

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
    cases = [sum([day["new_cases"]["total"] for day in d])]
    for slug in city_slugs:
        cases.append(sum([day["new_cases"][slug] for day in d]))
    return cases

# Calculates estimated active cases by town
def active_cases_by_town(d=today):
    output = []
    past_week = case_sum_list(data_days_ended(7, d))
    end_index = index_for_date(d)
    if past_week[0] > 0:
        for v in past_week:
            output.append(round(v/past_week[0]*daily_data[end_index]["active_cases"], 2))
    else:
        return [0, 0, 0, 0, 0]
    return output[1:]

# Scales a value to n per 100,000 population.
def per_100k(v):
    return v*100000/40117

# Calculates (if possible) the cases added by town over the n-day
# period ended on date d. Default is 7 days.
def cases_added(d, n=7):
    end_index = min(index_for_date(d), index_for_date(today))
    start_index = max(0, end_index-n+1)
    estimated = bool(daily_data[start_index]["estimates"]["cases"] or daily_data[end_index]["estimates"]["cases"])
    return {'value': sum([day["new_cases"]["total"] for day in daily_data[start_index:end_index+1]]), 'estimate': estimated}

# Returns a categorical risk level describing the risk of COVID-19
# in the county based on the average daily number of new cases over
# the past week per 100K population.
def risk_category(v):
    if v < 1:
        return "low"
    elif v < 10:
        return "moderate"
    elif v < 25:
        return "high"
    elif v < 75:
        return "critical"
    else:
        return "extreme"

# Calculates the vertical offset in pixels from the top of the risk
# meter on the homepage.
def risk_meter_offset(v):
    if risk_category(v) == "extreme":
        return -3
    elif risk_category(v) == "critical":
        # Calculate the "progress" between 25 and 75
        norm_v = 1-(v-25)/50
        offset = round(norm_v*36, 0)
        minimum = -3
    elif risk_category(v) == "high":
        # Same as above but between 10 and 25
        norm_v = 1-(v-10)/15
        offset = round(norm_v*36, 0)
        minimum = 32
    elif risk_category(v) == "moderate":
        # ...and between 1 and 10
        norm_v = 1-(v-1)/9
        offset = round(norm_v*36, 0)
        minimum = 68
    elif risk_category(v) == "low":
        # By definition, value here is already between 0 and 1
        offset = round((1-v)*36, 0)
        minimum = 104
    return minimum + offset

# Calculates (if possible) the tests added over the n-day period
# ended on date d. Default is 14 days.
def tests_added(d, n=14):
    end_index = min(index_for_date(d), index_for_date(today))
    start_index = max(0, end_index-n)
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
        start_index = max(0, end_index-n)
        estimated = bool(daily_data[start_index]["estimates"]["tests"] or daily_data[end_index]["estimates"]["tests"]\
            or daily_data[start_index+1]["estimates"]["cases"] or daily_data[end_index]["estimates"]["cases"])
        return {'value': float(round(cases/tests["value"]*100, 2)), 'estimate': estimated}
    return None

# Calculates the categorical risk level for the given date.
def risk_level(d):
    cases = case_sum_list(data_days_ended(14, d))[0]
    if cases is not None:
        average_daily_cases_14d_100k = per_100k(cases/14)
        return risk_category(average_daily_cases_14d_100k)
    return None

if __name__ == "__main__":
    # Calculate date-relative totals
    relative = dict()
    for i, day in enumerate(daily_data):
        cases_new = case_sum_list([day])
        cases_past_week = case_sum_list(data_days_ended(7, day["date"]))
        cases_mtd = case_sum_list(data_for_month(day["date"][:7], day["date"]))
        cases_ytd = case_sum_list(ytd_data(day["date"]))
        cases_cumulative = case_sum_list(daily_data[:i+1])
        cases_relative = [
            {'label': 'Today', 'totals': cases_new},
            {'label': 'Past Week', 'totals': cases_past_week},
            {'label': 'MTD', 'totals': cases_mtd},
            {'label': 'YTD', 'totals': cases_ytd},
            {'label': 'All', 'totals': cases_cumulative}
        ]
        relative[day["date"]] = cases_relative
    # Save the JSON file
    save_json(relative, 'data/relative.json')

    # Calculate monthly totals
    monthly_totals = dict()
    for i, day in enumerate(daily_data):
        monthly_totals[day["date"]] = [{'month': month, 'totals': case_sum_list(data_for_month(month, day["date"]))} for month in months_list(day["date"])]
    save_json(monthly_totals, 'data/monthly.json')

    # Calculate active cases by town
    active_by_town = dict()
    for i, day in enumerate(daily_data):
        active_by_town[day["date"]] = [{'town': cities[i+1], 'active': active_cases_by_town(day["date"])[i]} for i, _ in enumerate(active_cases_by_town())]
    save_json(active_by_town, 'data/active_town.json')

    # Calculate summary data
    summary = dict()
    for i, day in enumerate(daily_data):
        summary_day = dict()

        if i < 7:
            week_ago_day = None
        else:
            week_ago_day = daily_data[i-7]

        # Risk level and pask week average daily cases per 100K
        new_cases_7d = cases_added(day["date"])
        new_cases_14d = cases_added(day["date"], n=14)
        summary_day["risk_category"] = risk_level(day["date"])
        new_cases_14d_100k = per_100k(new_cases_14d["value"]/14)
        summary_day["new_cases_14d_100k"] = new_cases_14d_100k
        summary_day["risk_meter_offset"] = risk_meter_offset(new_cases_14d_100k)

        # New cases past week and change
        summary_day["new_cases_7d"] = new_cases_7d
        if week_ago_day is not None:
            new_cases_7d_week_ago = cases_added(daily_data[i-7]["date"])
            new_cases_7d_change = new_cases_7d["value"] - new_cases_7d_week_ago["value"]
            if new_cases_7d_week_ago["value"] != 0:
                new_cases_7d_change_percent = round(abs((new_cases_7d["value"] - new_cases_7d_week_ago["value"])/new_cases_7d_week_ago["value"])*100, 0)
            else:
                new_cases_7d_change_percent = None
            new_cases_7d_change_estimate = bool(new_cases_7d["estimate"] or new_cases_7d_week_ago["estimate"])
            if new_cases_7d_change_percent is not None:
                summary_day["new_cases_7d_change"] = {'value': new_cases_7d_change, 'percentage': new_cases_7d_change_percent, 'estimate': new_cases_7d_change_estimate}
            else:
                summary_day["new_cases_7d_change"] = {'value': new_cases_7d_change, 'estimate': new_cases_7d_change_estimate}

        # Active cases
        summary_day["active_cases"] = {'value': day["active_cases"], 'estimate': day["estimates"]["active"]}
        if week_ago_day is not None:
            active_cases_change = day["active_cases"] - week_ago_day["active_cases"]
            if week_ago_day["active_cases"] != 0:
                active_cases_change_percent = round(abs((day["active_cases"] - week_ago_day["active_cases"])/week_ago_day["active_cases"])*100, 0)
            else:
                active_cases_change_percent = None
            active_cases_change_estimate = bool(day["estimates"]["active"] or week_ago_day["estimates"]["active"])
            if active_cases_change_percent is not None:
                summary_day["active_cases_change"] = {'value': active_cases_change, 'percentage': active_cases_change_percent, 'estimate': active_cases_change_estimate}
            else:
                summary_day["active_cases_change"] = {'value': active_cases_change, 'estimate': active_cases_change_estimate}

        # Positivity rate
        if positivity_rate(day["date"]) is not None:
            summary_day["positivity_rate_2w"] = positivity_rate(day["date"])
            if positivity_rate(week_ago_day["date"]) is not None:
                positivity_rate_2w_change = positivity_rate(day["date"])["value"] - positivity_rate(week_ago_day["date"])["value"]
                if positivity_rate(week_ago_day["date"])["value"] != 0:
                    positivity_rate_2w_change_percent = round(abs((positivity_rate(day["date"])["value"] - positivity_rate(week_ago_day["date"])["value"])/positivity_rate(week_ago_day["date"])["value"])*100, 0)
                else:
                    positivity_rate_2w_change_percent = None
                positivity_rate_2w_change_estimate = bool(positivity_rate(day["date"])["estimate"] or positivity_rate(week_ago_day["date"])["estimate"])
                if positivity_rate_2w_change_percent is not None:
                    summary_day["positivity_rate_2w_change"] = {'value': positivity_rate_2w_change, 'percentage': positivity_rate_2w_change_percent, 'estimate': positivity_rate_2w_change_estimate}
                else:
                    summary_day["positivity_rate_2w_change"] = {'value': positivity_rate_2w_change, 'estimate': positivity_rate_2w_change_estimate}

        # Hospitalizations
        if day["hospitalizations"] is not None:
            summary_day["hospitalizations"] = {'value': day["hospitalizations"], 'estimate': day["estimates"]["hospitalizations"]}
            if week_ago_day is not None and week_ago_day["hospitalizations"] is not None:
                hospitalizations_change = day["hospitalizations"] - week_ago_day["hospitalizations"]
                if week_ago_day["hospitalizations"] != 0:
                    hospitalizations_change_percent = round(abs((day["hospitalizations"] - week_ago_day["hospitalizations"])/week_ago_day["hospitalizations"])*100, 0)
                else:
                    hospitalizations_change_percent = None
                hospitalizations_change_estimate = bool(day["estimates"]["hospitalizations"] or week_ago_day["estimates"]["hospitalizations"])
                if hospitalizations_change_percent is not None:
                    summary_day["hospitalizations_change"] = {'value': hospitalizations_change, 'percentage': hospitalizations_change_percent, 'estimate': hospitalizations_change_estimate}
                else:
                    summary_day["hospitalizations_change"] = {'value': hospitalizations_change, 'estimate': hospitalizations_change_estimate}

        # Deaths
        if day["deaths"] is not None:
            summary_day["deaths"] = {'value': day["deaths"], 'estimate': day["estimates"]["deaths"]}
            if week_ago_day is not None and week_ago_day["deaths"] is not None:
                deaths_change = day["deaths"] - week_ago_day["deaths"]
                deaths_change_estimate = bool(day["estimates"]["deaths"] or week_ago_day["estimates"]["deaths"])
                summary_day["deaths_change"] = {'value': deaths_change, 'estimate': deaths_change_estimate}

        if tests_added(day["date"], n=7) is not None:
            new_tests_7d = tests_added(day["date"], n=7)
            summary_day["new_tests_7d"] = tests_added(day["date"], n=7)
            if week_ago_day is not None and tests_added(week_ago_day["date"], n=7) is not None:
                new_tests_7d_week_ago = tests_added(week_ago_day["date"], n=7)
                new_tests_7d_change = new_tests_7d["value"] - new_tests_7d_week_ago["value"]
                if new_tests_7d_week_ago["value"] != 0:
                    new_tests_7d_change_percent = round(abs((new_tests_7d["value"] - new_tests_7d_week_ago["value"])/new_tests_7d_week_ago["value"])*100, 0)
                else:
                    new_tests_7d_change_percent = None
                new_tests_7d_change_estimate = bool(new_tests_7d["estimate"] or new_tests_7d_week_ago["estimate"])
                if new_tests_7d_change_percent is not None:
                    summary_day["new_tests_7d_change"] = {'value': new_tests_7d_change, 'percentage': new_tests_7d_change_percent, 'estimate': new_tests_7d_change_estimate}
                else:
                    summary_day["new_tests_7d_change"] = {'value': new_tests_7d_change, 'estimate': new_tests_7d_change_estimate}

        # Set some flags for hiding charts when needed
        if week_ago_day is None:
            # Days for which all charts should be hidden
            summary_day["hide_charts"] = 'all'
        elif i < 147:
            # Days for which testing charts should be hidden
            summary_day["hide_charts"] = 'test'
        elif i < 161:
            # Days for which the positivity rate chart should be hidden
            summary_day["hide_charts"] = 'pos_rate'

        # Add the previous/next dates as appropriate
        if i == 0:
            summary_day["next_date"] = daily_data[i+1]["date"]
        elif i == len(daily_data)-1:
            summary_day["prev_date"] = daily_data[i-1]["date"]
        else:
            summary_day["prev_date"] = daily_data[i-1]["date"]
            summary_day["next_date"] = daily_data[i+1]["date"]

        summary[day["date"]] = summary_day
    summary["last_updated"] = today
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
        if day["hospitalizations"] is not None:
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
            chart_day["average_daily_cases_7d"] = round(sum([day_data["new_cases"]["total"] for day_data in daily_data[i-6:i+1]])/7, 1)
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
                if daily_data[i-14]["tests"] is not None:
                    chart_day["tests"]["average_14d"] = round((daily_data[i]["tests"] - daily_data[i-14]["tests"])/14, 1)
        # Where possible, calculate the 14D positivity rate and risk level
        if positivity_rate(day["date"]) is not None:
            chart_day["positivity_rate"] = positivity_rate(day["date"])["value"]
        chart_data.append(chart_day)
    save_json(chart_data, 'assets/js/chart-data.json')