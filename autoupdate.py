import json
import os
import sys
sys.path.append(os.path.realpath('.'))
from process import cases_added, tests_added, daily_data, mtd_data
import urllib.request

last_date = daily_data[-1]["date"]

# URLs for the necessary data from the HCHD dashboard API
date_uri = "https://services.engagementnetwork.org/api-report/v1/indicator/MOCountyCovid/16005?area_ids=05000US29091&area_type=geoid&output_chart=0&output_desc=0&output_source=0" # Update date

with urllib.request.urlopen(date_uri) as date_url:
    # If the most recent update is already present the data files, exit immediately
    date_json = json.loads(date_url.read().decode())
    date = date_json["data"]["summary"]["values"][1][:10]
    if date in [day["date"] for day in daily_data]:
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

old_wp_total = sum([day["new_cases"]["west_plains"] for day in daily_data])
old_ws_total = sum([day["new_cases"]["willow_springs"] for day in daily_data])
old_mv_total = sum([day["new_cases"]["mountain_view"] for day in daily_data])
old_other_total = sum([day["new_cases"]["other"] for day in daily_data])
old_hc_total = old_wp_total + old_ws_total + old_mv_total + old_other_total

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
    hospitalizations = int(hospitalizations_data["data"]["summary"]["values"][1].replace(',', ''))

print('Total cases: '+str(total_cases)+' (+'+str(new_cases)+')')
print('Active cases: '+str(active_cases))
print('Hospitalizations: '+str(hospitalizations))
print('Deaths: '+str(deaths))

with urllib.request.urlopen(town_uri) as town_url:
    # Get total cases by town
    town_data = json.loads(town_url.read().decode())
    new_wp_cases = int(town_data["data"]["county_list"][13]["values"][2].replace(',', '')) - old_wp_total
    new_ws_cases = int(town_data["data"]["county_list"][14]["values"][2].replace(',', '')) - old_ws_total
    new_mv_cases = int(town_data["data"]["county_list"][8]["values"][2].replace(',', '')) - old_mv_total
    new_other_cases = new_cases - new_wp_cases - new_ws_cases - new_mv_cases

# Estimate new tests
old_cases_added_14d = cases_added(last_date, n=14)["value"]
old_tests_added_14d = tests_added(last_date, n=14)["value"]
new_cases_added_14d = cases_added(last_date, n=13)["value"] + total_cases - old_hc_total
# 14D positivity rate maintained by tests_new = cases_new / cases_old * tests_old
new_tests_added_14d = int(round(new_cases_added_14d / old_cases_added_14d * old_tests_added_14d, 0))
# Tests to subtract for the prior 13 days to get to the estimated new tests
new_tests_added_13d = tests_added(last_date, n=13)["value"]
new_tests_est = max(total_cases - old_hc_total, new_tests_added_14d - new_tests_added_13d)
total_tests_est = daily_data[-1]["tests"] + new_tests_est
print('Tests (est.): '+str(total_tests_est)+' (+'+str(new_tests_est)+')')

# Create new data dictionary to append to the daily data file
new_data = {
    'date': date,
    'new_cases': {
        'west_plains': new_wp_cases,
        'willow_springs': new_ws_cases,
        'mountain_view': new_mv_cases,
        'other': new_other_cases
    },
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
    'sources': None
}

if date[:7] != last_date[:7]:
    # If we have entered a new month, MTD data will be empty (the mtd_data() function 
    # from process.py will return the previous month's data, which is fine for that 
    # script but not this one)
    mtd = []
else:
    mtd = mtd_data()
mtd.append(new_data)

# Append the new data to the data file
with open(data_path, 'w+') as data_file:
    data_file.write(json.dumps(mtd, separators=(',', ':')))
    print('Saved '+data_path)