import json
import os
import sys
from utilities.calc import case_sums
sys.path.append(os.path.realpath('.'))
# from process import cases_added, tests_added, daily_data, mtd_data
from utilities import utilities
import urllib.request

last_date = utilities.data.today

# URLs for the necessary data from the HCHD dashboard API
date_uri = "https://services.engagementnetwork.org/api-report/v1/indicator/MOCountyCovid/16005?area_ids=05000US29091&area_type=geoid&output_chart=0&output_desc=0&output_source=0" # Update date

with urllib.request.urlopen(date_uri) as date_url:
    # If the most recent update is already present the data files, exit immediately
    date_json = json.loads(date_url.read().decode())
    date = date_json["data"]["summary"]["values"][1][:10]
    if date in [day["date"] for day in utilities.data.all]:
        print('Already have data for '+date+'. Exiting.')
        sys.exit()
    else:
        print('Updating daily data file for '+date+'...')

data_path = 'daily-data/'+date[:7]+'.json'
if not os.path.exists(data_path):
    # If the file we need doesn't already exist, create an empty one
    with open(data_path, 'w+') as f:
        f.write(json.dumps([]))

cases_uri = "https://services.engagementnetwork.org/api-report/v1/indicator/MOCountyCovid/16002?area_ids=05000US29091&area_type=geoid&output_chart=0&output_desc=0&output_source=0" # Active/total cases and deaths
hospitalizations_uri = "https://services.engagementnetwork.org/api-report/v1/indicator/MOCountyCovid/16006?area_ids=05000US29091&area_type=geoid&output_chart=0&output_desc=0&output_source=0" # Hospitalizations
town_uri = "https://services.engagementnetwork.org/api-report/v1/indicator/MOCountyCovid/16007?area_ids=05000US29091&area_type=geoid&output_chart=0&output_desc=0&output_source=0" # Total cases by town

old_hc_total = case_sums(utilities.data.all)["howell_county"]

with urllib.request.urlopen(cases_uri) as cases_url:
    # Get total cases, active cases, and deaths
    cases_data = json.loads(cases_url.read().decode())
    total_cases = int(cases_data["data"]["summary"]["values"][1].replace(',', ''))
    new_cases = total_cases - old_hc_total
    active_cases = int(cases_data["data"]["summary"]["values"][2].replace(',', ''))
    deaths = int(cases_data["data"]["summary"]["values"][4].replace(',', ''))

with urllib.request.urlopen(hospitalizations_uri) as hospitalizations_url:
    # Get hospitalizations
    hospitalizations_data = json.loads(hospitalizations_url.read().decode())
    try:
        hospitalizations = int(hospitalizations_data["data"]["summary"]["values"][1].replace(',', ''))
    except KeyError:
        hospitalizations = 0

print('Total cases: '+str(total_cases)+' (+'+str(new_cases)+')')
print('Active cases: '+str(active_cases))
print('Hospitalizations: '+str(hospitalizations))
print('Deaths: '+str(deaths))

with urllib.request.urlopen(town_uri) as town_url:
    # Get total cases by town
    town_data = json.loads(town_url.read().decode())

    towns = [item["values"][1].lower().strip() for item in town_data["data"]["county_list"]]
    town_dict = {
        "bakersfield": towns.index("bakersfield"),
        "brandsville": towns.index("brandsville"),
        "cabool": towns.index("cabool"),
        "caulfield": towns.index("caulfield"),
        "dora": towns.index("dora"),
        "koshkonong": towns.index("koshkonong"),
        "moody": towns.index("moody"),
        "mountain_view": towns.index("mountain view"),
        "peace_valley": towns.index("peace valley"),
        "pomona": towns.index("pomona"),
        "pottersville": towns.index("pottersville"),
        "summersville": towns.index("summersville"),
        "west_plains": towns.index("west plains"),
        "willow_springs": towns.index("willow springs"),
        "unknown": towns.index("no city specified")
    }

    town_cases_dict = {}

    for town in town_dict:
        town_cases_dict[town] = 0
        old_total = sum([day["new_cases"][town] for day in utilities.data.all])
        try:
            new_total = int(town_data["data"]["county_list"][town_dict[town]]["values"][2].replace(',', ''))
        except ValueError:
            # Assume the new total is unchanged for now if the value is "Less than 10"
            new_total = old_total
        town_cases_dict[town] = new_total - old_total

    if sum(town_cases_dict.values()) < new_cases:
        # If there is a gap between the known total of new cases and the per-town totals, add them into "unknown"
        town_cases_dict["unknown"] += new_cases - sum(town_cases_dict.values())

# Estimate new tests
old_cases_added_14d = utilities.calc.cases_added(last_date["date"], n=14)["cases"]["howell_county"]
old_tests_added_14d = utilities.calc.tests_added(last_date["date"], n=14)["tests"]
new_cases_added_14d = utilities.calc.cases_added(last_date["date"], n=13)["cases"]["howell_county"] + total_cases - old_hc_total
# 14D positivity rate maintained by tests_new = cases_new / cases_old * tests_old
new_tests_added_14d = int(round(new_cases_added_14d / old_cases_added_14d * old_tests_added_14d, 0))
# Tests to subtract for the prior 13 days to get to the estimated new tests
new_tests_added_13d = utilities.calc.tests_added(last_date["date"], n=13)["tests"]
new_tests_est = max(total_cases - old_hc_total, new_tests_added_14d - new_tests_added_13d)
total_tests_est = last_date["tests"] + new_tests_est
print('Tests (est.): '+str(total_tests_est)+' (+'+str(new_tests_est)+')')

# Create new data dictionary to append to the daily data file
new_data = {
    'date': date,
    'new_cases': town_cases_dict,
    'active_cases': active_cases,
    'hospitalizations': hospitalizations,
    'deaths': deaths,
    'tests': total_tests_est,
    'estimates': {
        'cases': False,
        'active': False,
        'hospitalizations': False,
        'deaths': False,
        'tests': True
    },
    'vaccinations': None,
    'sources': None
}

if date[:7] != last_date["date"][:7]:
    # If we have entered a new month, MTD data will be empty (the mtd_data() function 
    # from process.py will return the previous month's data, which is fine for that 
    # script but not this one)
    mtd = []
else:
    mtd = utilities.data.mtd_data(date)
mtd.append(new_data)

# Append the new data to the data file
with open(data_path, 'w+') as data_file:
    data_file.write(json.dumps(mtd, separators=(',', ':')))
    print('Saved '+data_path)

# Create a file in /content for Time Machine
time_machine_path = 'content/time-machine/'+date+'.md'
with open(time_machine_path, 'w+') as time_machine_file:
    time_machine_file.write('---\ndate: '+date+'\nlayout: time-machine\n---')
    print('Saved '+time_machine_path)