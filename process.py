from utilities import utilities

data = utilities.data.all

if __name__ == "__main__":
    # Temporary compatibility for expected output format in Hugo source files for some data
    def __case_sum_list__(case_sums):
        return [case_sums["howell_county"], case_sums["west_plains"], case_sums["willow_springs"], case_sums["mountain_view"], case_sums["other"]]

    # Returns a list of months for the date
    def __months_list__(d):
        months = utilities.unique([day["date"][:7] for day in utilities.data.cumulative_data(d)])
        return months

    relative = {}
    monthly = {}
    active_by_town = {}
    summary = {}
    table_data = []
    chart_data = []

    # Last updated date
    summary["last_updated"] = utilities.data.today["date"]

    for i, day in enumerate(utilities.data.calculation):
        d = day["date"]
        print(f"Processing data for {d}...")
        week_ago_day = utilities.data.week_ago(d)

        # Calculate date-relative totals
        cases_new = utilities.calc.case_sums([utilities.data.data_for_date(d)])
        cases_past_week = utilities.calc.case_sums(utilities.data.data_for_days_ended(7, d))
        cases_mtd = utilities.calc.case_sums(utilities.data.mtd_data(d))
        cases_ytd = utilities.calc.case_sums(utilities.data.ytd_data(d))
        cases_all = utilities.calc.case_sums(utilities.data.cumulative_data(d))
        relative[d] = [
            {'label': 'Today', 'totals': __case_sum_list__(cases_new)},
            {'label': 'Past Week', 'totals': __case_sum_list__(cases_past_week)},
            {'label': 'MTD', 'totals': __case_sum_list__(cases_mtd)},
            {'label': 'YTD', 'totals': __case_sum_list__(cases_ytd)},
            {'label': 'All', 'totals': __case_sum_list__(cases_all)},
        ]

        # Calculate monthly totals
        monthly[d] = [{'month': month, 'totals': __case_sum_list__(utilities.calc.case_sums(utilities.data.data_for_month(month, d)))} for month in __months_list__(d)]

        # Calculate estimated active cases by town
        active_by_town_estimates = utilities.calc.active_cases_by_town(d)
        active_list = []
        for town in utilities.geo.towns:
            if active_by_town_estimates[town] > 0:
                town_name = utilities.geo.towns[town]["formatted"]
                if not utilities.geo.towns[town]["in_county"]:
                    town_name += "**"
                active_list.append({
                    'key': town.replace('_', '-'),
                    'town': town_name,
                    'active': active_by_town_estimates[town]
            })
        active_list = sorted(active_list, key=lambda i: i["town"])
        active_by_town[d] = active_list
        summary_day = {}
        
        # Risk level
        summary_day["risk_category"] = utilities.calc.risk_level(d)
        summary_day["new_cases_14d_100k"] = utilities.calc.per_100k(utilities.calc.cases_added(day["date"], n=14)["cases"]["howell_county"]/14)
        
        # CDC Level of Community Transmission
        summary_day["community_transmission"] = utilities.calc.community_transmission(d)

        # 7-day new cases and change
        new_cases_7d = utilities.calc.cases_added(d)
        summary_day["new_cases_7d"] = utilities.calc.summary_new_cases_7d(d)

        # Active cases
        summary_day["active_cases"] = utilities.calc.summary_active_cases(d)
        summary_day["active_cases_change"] = utilities.calc.summary_active_cases_change(d)

        # Vaccinations
        vaccinations_summary = utilities.calc.summary_vaccinations(d)
        if vaccinations_summary is not None:
            summary_day["completed_percentage"] = vaccinations_summary["completed_percentage"]
            summary_day["initiated_percentage"] = vaccinations_summary["initiated_percentage"]

        # Positivity rate
        positivity_rate_2w = utilities.calc.summary_positivity_rate(d, lag_days=3)
        positivity_rate_change = utilities.calc.summary_positivity_rate_change(d, lag_days=3)
        if positivity_rate_2w is not None:
            summary_day["positivity_rate_2w"] = positivity_rate_2w
        if positivity_rate_change is not None:
            summary_day["positivity_rate_2w_change"] = positivity_rate_change

        # Hospitalizations
        if utilities.calc.summary_hospitalizations(d) is not None:
            summary_day["hospitalizations"] = utilities.calc.summary_hospitalizations(d)
        if utilities.calc.summary_hospitalizations_change(d) is not None:
            summary_day["hospitalizations_change"] = utilities.calc.summary_hospitalizations_change(d)

        # Deaths
        if utilities.calc.summary_deaths(d) is not None:
            summary_day["deaths"] = utilities.calc.summary_deaths(d)
        if utilities.calc.summary_deaths_change(d) is not None:
            summary_day["deaths_change"] = utilities.calc.summary_deaths_change(d)

        # 7-day new tests
        if utilities.calc.summary_new_tests_7d(d) is not None:
            summary_day["new_tests_7d"] = utilities.calc.summary_new_tests_7d(d, lag_days=3)
        if utilities.calc.summary_new_tests_7d_change(d) is not None:
            summary_day["new_tests_7d_change"] = utilities.calc.summary_new_tests_7d_change(d, lag_days=3)

        # Add the previous/next dates as appropriate
        if i == 0:
            summary_day["next_date"] = utilities.data.all[i+1]["date"]
        elif i == len(utilities.data.all)-1:
            summary_day["prev_date"] = utilities.data.all[i-1]["date"]
        else:
            summary_day["prev_date"] = utilities.data.all[i-1]["date"]
            summary_day["next_date"] = utilities.data.all[i+1]["date"]

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
        
        summary[d] = summary_day

        # Table data
        table_data.append(utilities.calc.table_dict(d))

        # Chart data
        chart_data.append(utilities.calc.chart_dict(d))
    
    utilities.save_json(relative, 'data/relative.json')
    utilities.save_json(monthly, 'data/monthly.json')
    utilities.save_json(active_by_town, 'data/active_town.json')
    utilities.save_json(summary, 'data/summary.json')
    utilities.save_json(table_data, 'data/daily.json')
    utilities.save_json(chart_data, 'assets/js/chart-data.json')