from calendar import week
from copy import deepcopy
from utilities import data
from . import utilities

################# ARITHMETIC ##################

# Scales a value to n per 100,000 population.
def per_100k(v):
    populations = [utilities.geo.towns[town]["population"] for town in utilities.geo.towns if utilities.geo.towns[town]["population"] is not None]
    return v*100000/sum(populations)

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
    if utilities.date._date_is_before_(utilities.date._date_advanced_by_(end_date, -n), '2020-04-01'):
        return None
    data_slice = utilities.data.data_for_days_ended(n, end_date)
    # Find whether the return value is impacted by estimated data
    start_estimated = data_slice[0]["estimates"]["cases"]
    end_estimated = data_slice[-1]["estimates"]["cases"]
    estimated = bool(start_estimated or end_estimated)
    # Return case sums by town for the specified period
    return {"cases": case_sums(data_slice), "estimated": estimated}

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
    else:
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
    else:
        return None