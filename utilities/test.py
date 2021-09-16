import unittest
from utilities.calc import case_sums
import pytest
import json
from . import utilities

data_1 = utilities.data._data_in_file_("utilities/test-data/data-01.json")
data_2 = utilities.data._data_in_file_("utilities/test-data/data-02.json")
data_3 = utilities.data._data_in_file_("utilities/test-data/data-03.json")
data_all = utilities.data._data_in_file_("utilities/test-data/data-all.json")
utilities.data.all = data_all

class TestGenericMethods(unittest.TestCase):
    # Verify that only unique list members are returned by utilities.unique
    def test_unique(self):
        test_list = [-5, -3, -3, -2, -1, 0, 1, 1, 1, 1, 2, 3, 4, 4, 5]
        assert utilities.unique(test_list) == [-5, -3, -2, -1, 0, 1, 2, 3, 4, 5]

class TestDataMethods(unittest.TestCase):
    # Verify that the number of days in our static data files is what we expect
    def test_data_count(self):
        assert len(data_1) == 30
        assert len(data_2) == 31
        assert len(data_3) == 28

    def test_dates(self):
        # Create empty lists that we will fill with the expected dates for each data file
        dates_1 = []
        dates_2 = []
        dates_3 = []
        i = 1
        while i < 32:
            if i < 10:
                i_padded = "0"+str(i)
            else:
                i_padded = str(i)
            if i < 31:
                dates_1.append(f"2020-06-{i_padded}")
            if i < 29:
                dates_3.append(f"2021-02-{i_padded}")
            dates_2.append(f"2020-05-{i_padded}")
            i += 1
        # Verify that each of the dates in the data are in the lists
        data_1_dates = [d["date"] for d in data_1]
        for j, d in enumerate(dates_1):
            assert d in data_1_dates
            assert data_1_dates[j] in dates_1
        data_2_dates = [d["date"] for d in data_2]
        for j, d in enumerate(dates_2):
            assert d in data_2_dates
            assert data_2_dates[j] in dates_2
        data_3_dates = [d["date"] for d in data_3]
        for j, d in enumerate(dates_3):
            assert d in data_3_dates
            assert data_3_dates[j] in dates_3

    def test_data_for_date(self):
        test_1_date = "2020-06-07"
        test_1 = utilities.data.data_for_date(test_1_date)
        assert test_1["date"] == test_1_date
        test_2_date = "2020-05-30"
        test_2 = utilities.data.data_for_date(test_2_date)
        assert test_2["date"] == test_2_date
        test_3_date = "2021-02-14"
        test_3 = utilities.data.data_for_date(test_3_date)
        assert test_3["date"] == test_3_date

    def test_week_ago(self):
        # Test a date for which week-ago data exists
        test_date = "2020-06-14"
        test_exclusive = utilities.data.week_ago(test_date)
        assert test_exclusive["date"] == "2020-06-07"
        test_inclusive = utilities.data.week_ago(test_date, inclusive=True)
        assert test_inclusive["date"] == "2020-06-08"
        # Test a date for which week-ago data does not exist
        test_nonexistent_date = "2020-04-01"
        test_exclusive = utilities.data.week_ago(test_nonexistent_date)
        assert test_exclusive is None
        test_inclusive = utilities.data.week_ago(test_nonexistent_date, inclusive=True)
        assert test_inclusive is None

    def test_cumulative_data(self):
        assert len(utilities.data.cumulative_data('2020-04-01')) == 1
        assert len(utilities.data.cumulative_data('2020-06-30')) == 91

    def test_ytd_data(self):
        assert len(utilities.data.ytd_data('2020-06-30')) == 91
        assert len(utilities.data.ytd_data('2021-02-14')) == 45

    def test_mtd_data(self):
        assert len(utilities.data.mtd_data('2020-06-30')) == 30
        assert len(utilities.data.mtd_data('2021-02-14')) == 14

    def test_data_for_month(self):
        assert len(utilities.data.data_for_month('2021-02')) == 28
        assert len(utilities.data.data_for_month('2021-02', end_date='2021-02-14')) == 14

    def test_all_data(self):
        assert len(utilities.data.all) == 529

    def test_data_for_days_ended(self):
        data_days_ended = utilities.data.data_for_days_ended(7, end_date='2021-02-14')
        assert len(data_days_ended) == 7
        assert data_days_ended[0]["date"] == '2021-02-08'
        assert data_days_ended[-1]["date"] == '2021-02-14'

class TestDateMethods(unittest.TestCase):
    def test_is_before(self):
        assert not utilities.date.date_is_before('2021-01-01', '2021-01-01')
        assert not utilities.date.date_is_before('2021-01-08', '2021-01-01')
        assert utilities.date.date_is_before('2021-01-01', '2021-01-08')

    def test_date_components_int(self):
        assert utilities.date._date_components_int_('2021-01-08') == (2021, 1, 8)
    
    def test_days_in_month(self):
        assert utilities.date._days_in_month_('2020-02-01') == 29
        assert utilities.date._days_in_month_('2021-02-01') == 28
        assert utilities.date._days_in_month_('2021-04-01') == 30
        assert utilities.date._days_in_month_('2021-05-01') == 31

    def test_days_between_dates(self):
        assert utilities.date._days_between_dates_('2021-01-08', '2021-01-15') == 7

class TestCalculationMethods(unittest.TestCase):
    def test_per_100k(self):
        assert round(utilities.calc.per_100k(42), 2) == 103.96

    def test_cases_added(self):
        # Test a date from before the dataset begins
        assert utilities.calc.cases_added('2020-03-30')["cases"] == 0

    def test_case_sums(self):
        assert utilities.calc.case_sums(data_1)["howell_county"] == 32
        assert utilities.calc.case_sums(data_2)["howell_county"] == 2
        assert utilities.calc.case_sums(data_2)["west_plains"] == 0

    def test_case_sum_list(self):
        case_sums = utilities.calc.case_sums(data_1)
        assert utilities.calc.__case_sum_list__(case_sums) == [32, 16, 0, 5, 11]

    def test_active_cases_by_town(self):
        test_active_cases = utilities.calc.active_cases_by_town('2021-02-10')
        assert test_active_cases["mountain_view"] == 7
        assert test_active_cases["pomona"] == 1
        assert test_active_cases["pottersville"] == 1
        assert test_active_cases["west_plains"] == 36
        assert test_active_cases["willow_springs"] == 6
        test_active_cases_2 = utilities.calc.active_cases_by_town('2020-05-20')
        assert test_active_cases_2["west_plains"] == 0

    def test_risk_level(self):
        assert utilities.calc.risk_level('2020-04-01') == 'low'
        assert utilities.calc.risk_level('2020-06-11') == 'moderate'
        assert utilities.calc.risk_level('2020-07-30') == 'high'
        assert utilities.calc.risk_level('2020-11-11') == 'critical'
        assert utilities.calc.risk_level('2020-10-20') == 'extreme'

    def test_summary_new_cases(self):
        assert utilities.calc.summary_new_cases_7d('2020-04-01')["value"] == 1
        assert utilities.calc.summary_new_cases_7d('2021-07-01')["value"] == 77

    def test_summary_active_cases(self):
        assert utilities.calc.summary_active_cases('2020-04-01')["value"] == 1
        assert utilities.calc.summary_active_cases('2021-07-01')["value"] == 77
        assert utilities.calc.summary_active_cases_change('2020-04-01') is None
        assert "percentage" not in utilities.calc.summary_active_cases_change('2020-05-31')
        assert utilities.calc.summary_active_cases_change('2021-07-01')["value"] == 41
        assert round(utilities.calc.summary_active_cases_change('2021-07-01')["percentage"], 1) == 114.0

    def test_summary_tests(self):
        assert utilities.calc.summary_new_tests_7d('2020-03-04', lag_days=3)["value"] == 0
        assert utilities.calc.summary_new_tests_7d('2020-04-04', lag_days=3)["value"] == 17
        assert utilities.calc.summary_new_tests_7d_change('2020-04-01', lag_days=3) is None
        assert utilities.calc.summary_new_tests_7d('2021-02-05', lag_days=3)["value"] == 896
        assert utilities.calc.summary_new_tests_7d_change('2021-02-05', lag_days=3)["value"] == 29
        assert round(utilities.calc.summary_new_tests_7d_change('2021-02-05', lag_days=3)["percentage"], 1) == 3.0

    def test_summary_positivity_rate(self):
        assert utilities.calc.summary_positivity_rate('2020-03-30', lag_days=3) is None
        assert round(utilities.calc.summary_positivity_rate('2021-02-05', lag_days=3)["value"], 2) == 8.62
        assert utilities.calc.summary_positivity_rate_change('2020-04-02', lag_days=3) is None
        assert round(utilities.calc.summary_positivity_rate_change('2021-02-05', lag_days=3)["value"], 1) == -0.4

    def test_summary_hospitalizations(self):
        assert utilities.calc.summary_hospitalizations('2021-08-01')["value"] == 24
        assert utilities.calc.summary_hospitalizations('2020-04-01')["value"] == 0
        assert utilities.calc.summary_hospitalizations_change('2020-04-01') is None
        assert "percentage" not in utilities.calc.summary_hospitalizations_change('2020-07-21')
        assert utilities.calc.summary_hospitalizations_change('2021-07-01')["value"] == 0

    def test_summary_deaths(self):
        assert utilities.calc.summary_deaths('2021-08-01')["value"] == 103
        assert utilities.calc.summary_deaths('2020-04-01')["value"] == 0
        assert utilities.calc.summary_deaths_change('2020-04-01') is None
        assert utilities.calc.summary_deaths_change('2021-07-01')["value"] == 1

    def test_summary_vaccinations(self):
        assert utilities.calc.summary_vaccinations('2020-05-20') is None
        assert utilities.calc.summary_vaccinations('2021-05-20')["completed_percentage"] == 16.3
        assert utilities.calc.summary_vaccinations('2021-05-20')["initiated_percentage"] == 3.32

    def test_community_transmission(self):
        assert utilities.calc.community_transmission('2020-05-20') == 'low'
        assert utilities.calc.community_transmission('2020-08-14') == 'moderate'
        assert utilities.calc.community_transmission('2020-08-24') == 'considerable'
        assert utilities.calc.community_transmission('2020-08-30') == 'high'

    def test_table_data(self):
        test_data = utilities.calc.table_dict('2021-03-02')
        assert test_data["total_cases"]["west_plains"] == 2394
        assert test_data["new_cases"] == 2
        assert test_data["active_cases"] == 26
        assert test_data["hospitalizations"] == 7
        assert test_data["tests"]["total"] == 30780
        assert test_data["tests"]["new"] == 59
        assert test_data["positivity_rate"]["value"] == 4.48
        assert test_data["doses"] == 309
        assert test_data["initiated"] == 4670
        assert test_data["completed"] == 2915
        test_no_sources = utilities.calc.table_dict('2020-11-28')
        assert test_no_sources["sources"] is None

    def test_chart_data(self):
        test_data = utilities.calc.chart_dict('2021-03-02')
        assert test_data["c"]["west_plains"] == 2394
        assert test_data["n"]["west_plains"] == 2
        assert test_data["n_7d_av"] == 4.3
        assert test_data["n_14d_av_100k"] == 12.2
        assert test_data["a"] == 26
        assert test_data["a_7d_av"] == 34.1
        assert test_data["h"] == 7
        assert test_data["t"]["14d_av"] == 110.1
        assert test_data["p"] == 4.48
        assert test_data["vd"] == 309
        assert test_data["vd_7d_av"] == 300.9
        assert test_data["vi"] == 4670
        assert test_data["vc"] == 2915