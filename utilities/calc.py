from calendar import week
from copy import deepcopy
from utilities.data import week_ago
from . import utilities

################# ARITHMETIC ##################

# Scales a value to n per 100,000 population.
def per_100k(v):
    populations = [utilities.geo.towns[town]["population"] for town in utilities.geo.towns if utilities.geo.towns[town]["population"] is not None]
    return v*100000/sum(populations)

################# UTILITIES ###################

def __summary_dict__(value, estimated, percentage=None):
    if percentage is None:
        return {'value': value, 'estimate': estimated}
    return {'value': value, 'percentage': percentage, 'estimate': estimated}

def __week_ago_day__(d):
    return utilities.data.week_ago(d)

# Temporary compatibility for expected output format in Hugo source files for some data
def __case_sum_list__(case_sums):
    return [case_sums["howell_county"], case_sums["west_plains"], case_sums["willow_springs"], case_sums["mountain_view"], case_sums["other"]]

__city_slugs_county__ = ["county", "west_plains", "willow_springs", "mountain_view", "other"]

############## NEW/ACTIVE CASES ###############

# Returns a dictionary with case sums for the given data slice by town as well as Howell County and "other" totals.
def case_sums(data_slice):
    case_sums = {}
    for town in utilities.geo.towns:
        case_sums[town] = sum([day["new_cases"][town] for day in data_slice])
    for group in utilities.geo.groups:
        case_sums[group] = 0
        for town in utilities.geo.groups[group]["towns"]:
            case_sums[group] += sum([day["new_cases"][town] for day in data_slice])
    return case_sums

# Calculates estimated active cases by town
def active_cases_by_town(date):
    output = {}
    past_week_sum = case_sums(utilities.data.data_for_days_ended(7, date))
    for town in utilities.geo.towns:
        if past_week_sum["howell_county"] > 0:
            output[town] = int(round(past_week_sum[town]/past_week_sum["howell_county"]*utilities.data.data_for_date(date)["active_cases"], 0))
        else:
            output[town] = 0
    for group in utilities.geo.groups:
        output[group] = 0
        for town in utilities.geo.groups[group]["towns"]:
            if past_week_sum["howell_county"] > 0:
                output[group] += int(round(past_week_sum[town]/past_week_sum["howell_county"]*utilities.data.data_for_date(date)["active_cases"], 0))
            else:
                output[group] = 0
    return output

# Calculates (if possible) the cases added by town over the n-day
# period ended on date d. Default is 7 days.
def cases_added(end_date, n=7):
    data_slice = utilities.data.data_for_days_ended(n, end_date)
    # Find whether the return value is impacted by estimated data
    start_estimated = data_slice[0]["estimates"]["cases"]
    end_estimated = data_slice[-1]["estimates"]["cases"]
    estimated = bool(start_estimated or end_estimated)
    # Return case sums by town for the specified period
    return {"cases": case_sums(data_slice), "estimated": estimated}

# Returns a dictionary for new cases added in the week prior to the given date.
def summary_new_cases_7d(d):
    new_cases_7d = cases_added(d)
    return __summary_dict__(new_cases_7d["cases"]["howell_county"], new_cases_7d["estimated"])

# Returns a dictionary for the change in new cases added in the past week
# relative to one week prior to the given date.
def summary_new_cases_7d_change(d):
    new_cases_7d = cases_added(d)
    week_ago_day = __week_ago_day__(d)
    if week_ago_day is not None:
        new_cases_7d_week_ago = cases_added(utilities.date._date_advanced_by_(d, -7))
        new_cases_7d_change = new_cases_7d["cases"]["howell_county"] - new_cases_7d_week_ago["cases"]["howell_county"]
        if new_cases_7d_week_ago["cases"]["howell_county"] != 0:
            new_cases_7d_change_percent = int(round(abs((new_cases_7d["cases"]["howell_county"] - new_cases_7d_week_ago["cases"]["howell_county"])/new_cases_7d_week_ago["cases"]["howell_county"])*100, 0))
        else:
            new_cases_7d_change_percent = None
        new_cases_7d_change_estimate = bool(new_cases_7d["estimated"] or new_cases_7d_week_ago["estimated"])
        return __summary_dict__(new_cases_7d_change, new_cases_7d_change_estimate, new_cases_7d_change_percent)

# Returns a dictionary for active cases on the given date.
def summary_active_cases(d):
    return __summary_dict__(utilities.data.data_for_date(d)["active_cases"], utilities.data.today["estimates"]["active"])

# Returns a dictionary for active cases on the given date.
def summary_active_cases_change(d):
    day_data = utilities.data.data_for_date(d)
    week_ago_day = __week_ago_day__(d)
    if week_ago_day is not None:
        active_cases_change = day_data["active_cases"] - week_ago_day["active_cases"]
        if week_ago_day["active_cases"] != 0:
            active_cases_change_percent = round(abs((day_data["active_cases"] - week_ago_day["active_cases"])/week_ago_day["active_cases"])*100, 0)
        else:
            active_cases_change_percent = None
        active_cases_change_estimate = bool(day_data["estimates"]["active"] or week_ago_day["estimates"]["active"])
        return __summary_dict__(active_cases_change, active_cases_change_estimate, active_cases_change_percent)
    return None
    
################# RISK LEVEL ##################

def __risk_level_value__(d):
    cases = case_sums(utilities.data.data_for_days_ended(14, d))["howell_county"]
    if cases is not None:
        return per_100k(cases/14)
    return None

# Finds the categorical risk level for the given date.
def risk_level(d):
    cases = case_sums(utilities.data.data_for_days_ended(14, d))["howell_county"]
    if cases is not None:
        average_daily_cases_14d_100k = per_100k(cases/14)
        if average_daily_cases_14d_100k < 1:
            return "low"
        elif average_daily_cases_14d_100k < 10:
            return "moderate"
        elif average_daily_cases_14d_100k < 25:
            return "high"
        elif average_daily_cases_14d_100k < 75:
            return "critical"
        else:
            return "extreme"
    return None

# Calculates the horizontal offset in pixels from the top of the risk
# meter on the homepage.
def risk_meter_offset(d):
    v = __risk_level_value__(d)
    if risk_level(d) == "extreme":
        return -3
    elif risk_level(d) == "critical":
        # Calculate the "progress" between 25 and 75
        norm_v = 1-(v-25)/50
        offset = round(norm_v*36, 0)
        minimum = -3
    elif risk_level(d) == "high":
        # Same as above but between 10 and 25
        norm_v = 1-(v-10)/15
        offset = round(norm_v*36, 0)
        minimum = 32
    elif risk_level(d) == "moderate":
        # ...and between 1 and 10
        norm_v = 1-(v-1)/9
        offset = round(norm_v*36, 0)
        minimum = 68
    elif risk_level(d) == "low":
        # By definition, value here is already between 0 and 1
        offset = round((1-v)*36, 0)
        minimum = 104
    return minimum + offset

########### TESTS/POSITIVITY RATE #############

# Calculates (if possible) the tests added by town over the n-day
# period ended on date d. Default is 7 days.
def tests_added(end_date, n=7):
    data_slice = utilities.data.data_for_days_ended(n+1, end_date)
    if data_slice[0]["tests"] is not None:
        # Find whether the return value is impacted by estimated data
        start_estimated = data_slice[0]["estimates"]["tests"]
        end_estimated = data_slice[-1]["estimates"]["tests"]
        estimated = bool(start_estimated or end_estimated)
        # Return tests added for the specified period
        return {"tests": data_slice[-1]["tests"] - data_slice[0]["tests"], "estimated": estimated}
    return None

# Calculates the positivity rate over the n days ended on date d.
# Default is 14 days.
def positivity_rate(end_date, n=14):
    new_cases = cases_added(end_date, n)
    new_tests = tests_added(end_date, n)
    if new_tests is not None:
        # Find whether the return value is impacted by estimated data
        estimated = bool(new_cases["estimated"] or new_tests["estimated"])
        # Return tests added for the specified period
        return {"positivity_rate": round(new_cases["cases"]["howell_county"]/new_tests["tests"]*100, 2), "estimated": estimated}
    return None

def summary_positivity_rate(d):
    current_positivity_rate = positivity_rate(d)
    if current_positivity_rate is not None:
        return __summary_dict__(current_positivity_rate["positivity_rate"], current_positivity_rate["estimated"])
    return None

def summary_positivity_rate_change(d):
    current_positivity_rate = positivity_rate(d)
    week_ago_day = __week_ago_day__(d)
    if week_ago_day is not None and current_positivity_rate is not None:
        week_ago_positivity_rate = positivity_rate(week_ago_day["date"])
        if week_ago_positivity_rate is not None:
            positivity_rate_2w_change = current_positivity_rate["positivity_rate"] - week_ago_positivity_rate["positivity_rate"]
            if week_ago_positivity_rate["positivity_rate"] != 0:
                positivity_rate_2w_change_percent = int(round(abs((current_positivity_rate["positivity_rate"] - week_ago_positivity_rate["positivity_rate"])/week_ago_positivity_rate["positivity_rate"])*100, 0))
            else:
                positivity_rate_2w_change_percent = None
            positivity_rate_2w_change_estimate = bool(current_positivity_rate["estimated"] or week_ago_positivity_rate["estimated"])
            return __summary_dict__(positivity_rate_2w_change, positivity_rate_2w_change_estimate, positivity_rate_2w_change_percent)
    return None

def summary_new_tests_7d(d):
    if tests_added(d, n=7) is not None:
        new_tests_7d = tests_added(d, n=7)
        return __summary_dict__(new_tests_7d["tests"], new_tests_7d["estimated"])

def summary_new_tests_7d_change(d):
    new_tests_7d = tests_added(d, n=7)
    week_ago_day = __week_ago_day__(d)
    if new_tests_7d is not None and week_ago_day is not None and tests_added(week_ago_day["date"], n=7) is not None:
        new_tests_7d_week_ago = tests_added(week_ago_day["date"], n=7)
        new_tests_7d_change = new_tests_7d["tests"] - new_tests_7d_week_ago["tests"]
        if new_tests_7d_week_ago["tests"] != 0:
            new_tests_7d_change_percent = round(abs((new_tests_7d["tests"] - new_tests_7d_week_ago["tests"])/new_tests_7d_week_ago["tests"])*100, 0)
        else:
            new_tests_7d_change_percent = None
        new_tests_7d_change_estimate = bool(new_tests_7d["estimated"] or new_tests_7d_week_ago["estimated"])
        return __summary_dict__(new_tests_7d_change, new_tests_7d_change_estimate, new_tests_7d_change_percent)
    return None

############## HOSPITALIZATIONS ###############
def summary_hospitalizations(d):
    data = utilities.data.data_for_date(d)
    if data["hospitalizations"] is not None:
        return __summary_dict__(data["hospitalizations"], data["estimates"]["hospitalizations"])
    return None

def summary_hospitalizations_change(d):
    data = utilities.data.data_for_date(d)
    week_ago_day = __week_ago_day__(d)
    if week_ago_day is not None and week_ago_day["hospitalizations"] is not None:
        hospitalizations_change = data["hospitalizations"] - week_ago_day["hospitalizations"]
        if week_ago_day["hospitalizations"] != 0:
            hospitalizations_change_percent = round(abs((data["hospitalizations"] - week_ago_day["hospitalizations"])/week_ago_day["hospitalizations"])*100, 0)
        else:
            hospitalizations_change_percent = None
        hospitalizations_change_estimate = bool(data["estimates"]["hospitalizations"] or week_ago_day["estimates"]["hospitalizations"])
        return __summary_dict__(hospitalizations_change, hospitalizations_change_estimate, hospitalizations_change_percent)
    return None

################### DEATHS ####################
def summary_deaths(d):
    data = utilities.data.data_for_date(d)
    if data["deaths"] is not None:
        return __summary_dict__(data["deaths"], data["estimates"]["deaths"])
    return None

def summary_deaths_change(d):
    data = utilities.data.data_for_date(d)
    week_ago_day = __week_ago_day__(d)
    if week_ago_day is not None and week_ago_day["deaths"] is not None:
        deaths_change = data["deaths"] - week_ago_day["deaths"]
        deaths_change_estimate = bool(data["estimates"]["deaths"] or week_ago_day["estimates"]["deaths"])
        return __summary_dict__(deaths_change, deaths_change_estimate)
    return None

############## TABLE/CHART DATA ###############
def table_dict(d):
    data = utilities.data.data_for_date(d)
    prev_day = utilities.data.data_for_date(utilities.date._date_advanced_by_(d, -1))
    table_day = {}
    # Transfer date key
    table_day["date"] = data["date"]
    # Calculate total and new cases
    total_cases = __case_sum_list__(utilities.calc.case_sums(utilities.data.all))
    new_cases = __case_sum_list__(utilities.calc.case_sums([utilities.data.data_for_date(d)]))
    table_day["total_cases"] = dict(zip(__city_slugs_county__, total_cases))
    table_day["new_cases"] = dict(zip(__city_slugs_county__, new_cases))
    # Transfer active cases, hospitalizations, deaths, source links, and estimates
    table_day["active_cases"] = data["active_cases"]
    if data["hospitalizations"] is not None:
        table_day["hospitalizations"] = data["hospitalizations"]
    table_day["deaths"] = data["deaths"]
    table_day["estimates"] = data["estimates"]
    # Where possible, add in total/new tests
    table_day["tests"] = dict()
    if data["tests"] is not None:
        table_day["tests"]["total"] = data["tests"]
        if prev_day is not None and prev_day["tests"] is not None:
            table_day["tests"]["new"] = data["tests"] - prev_day["tests"]
    # Where possible, calculate the 14D positivity rate and risk level
    if utilities.calc.positivity_rate(d) is not None:
        table_day["positivity_rate"] = utilities.calc.summary_positivity_rate(d)
    if utilities.calc.risk_level(d) is not None:
        table_day["risk_level"] = utilities.calc.risk_level(d)
    # Transfer sources key
    if data["sources"] is not None:
        table_day["sources"] = [{'number': j, 'url': source} for j, source in enumerate(data["sources"], start=1)]
    else:
        table_day["sources"] = None
    return table_day

def chart_dict(d):
    data = utilities.data.data_for_date(d)
    data_past_week = utilities.data.data_for_days_ended(7, d)
    prev_day = utilities.data.data_for_date(utilities.date._date_advanced_by_(d, -1))
    prev_2w_ago = utilities.data.data_for_date(utilities.date._date_advanced_by_(d, -14))
    # Chart data
    chart_day = {}
    # Transfer date key
    chart_day["date"] = data["date"]
    # Calculate total and new cases
    chart_day["total_cases"] = dict(zip(__city_slugs_county__, __case_sum_list__(case_sums(utilities.data.cumulative_data(d)))))
    chart_day["new_cases"] = dict(zip(__city_slugs_county__, __case_sum_list__(case_sums([utilities.data.data_for_date(d)]))))
    # Calculate 7D average new cases
    chart_day["average_daily_cases_7d"] = round(case_sums(data_past_week)["howell_county"]/7, 1)
    # Transfer active cases
    chart_day["active_cases"] = data["active_cases"]
    # Calculate 7D average active cases
    chart_day["average_active_cases_7d"] = round(sum([day_data["active_cases"] for day_data in data_past_week])/7, 1)
    # Where possible, add in total/new tests
    chart_day["tests"] = dict()
    if data["tests"] is not None:
        chart_day["tests"]["total"] = data["tests"]
        if prev_day["tests"] is not None:
            chart_day["tests"]["new"] = data["tests"] - prev_day["tests"]
            if prev_2w_ago["tests"] is not None:
                chart_day["tests"]["average_14d"] = round((data["tests"] - prev_2w_ago["tests"])/14, 1)
    # Where possible, calculate the 14D positivity rate and risk level
    if positivity_rate(data["date"]) is not None:
        chart_day["positivity_rate"] = positivity_rate(data["date"])["positivity_rate"]
    return chart_day