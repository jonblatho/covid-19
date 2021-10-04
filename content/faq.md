---
title: FAQ
menu: main
---

## Frequently Asked Questions

### Where does this data come from?
Most data here comes from daily reports published by the Howell County Health Department (HCHD) on their [dashboard](https://allthingsmissouri.org/county-covid-19-dashboards/howell-county/) and their [Facebook page](https://www.facebook.com/Howell-County-Health-Department-170310842983730). Vaccination and testing data comes from the Missouri Department of Health and Senior Services (DHSS) [vaccine metrics](https://health.mo.gov/living/healthcondiseases/communicable/novel-coronavirus/data/data-download-vaccine.php) and [public health metrics](https://health.mo.gov/living/healthcondiseases/communicable/novel-coronavirus/data/data-download.php) pages. Sources corresponding to data, when available, are linked in the [All Data](../all-data) table.

### Why don't daily case counts here match the HCHD dashboard?
Since case data on this dashboard is stored by town and the HCHD only reports the total number of cases per town each day, cases fall under the report date here, while on the HCHD dashboard dates cases correspond to the test date. Usually, the difference is within a few days.

### When is this site updated?
Subject to the availability of new data, the site is updated three times a day, twice automatically and once manually:
* **Automatic update #1:** Every day, data on cases, hospitalizations, and deaths is pulled in from the HCHD dashboard automatically. To allow for possible failures, three attempts are made to pull in data automatically, the first of which occurs around 10:35 PM CDT.
* **Automatic update #2:** Overnight each day, data on testing and vaccinations is pulled in from the state DHSS website automatically. This occurs shortly after 5 AM CDT or 4 AM CST.
* **Manual update:** By each non-holiday weekday evening, the site is updated to add a link to the HCHD Facebook post corresponding to the most recent automatic updates, if available.

I am a human, so sometimes I must run late or miss a day on manual updates. If I do, I will catch things up as soon as I can.

You can always confirm the time the site was most recently updated by checking the "Site last updated" line in the footer on the homepage.

### What data is estimated, and how?
Testing data is estimated on automatic updates because the actual test count is not published until the following weekday. In the absense of an actual test count, the number of new tests is estimated by holding the 14-day positivity rate as close to constant as possible.

When there is a gap in data reporting, such as a weekend, I may apply estimates by assuming the number changed linearly between the start and end values across the reporting gap. Estimated data is reflected in the [All Data](../all-data) table with italic text.

Data for active cases by town is estimated by normalizing the 7-day total new cases for the county and categories (cities and “other”) and multiplying the county total active cases by those normalized values. Rounding may cause the sum of the by-town values not to exactly equal the county total. Estimates for active cases by town are hidden when there are few active cases in the county.

### How does data by town work?
Data by town is based on ZIP Code, not city limits. Therefore, for example, while the population of the city of West Plains is about 12,000, its ZIP Code population is actually 24,554 based on 2010 Census data (for the sections of the 65775 ZIP code within Howell County). For Willow Springs and Mountain View, these populations are 5,414 and 5,382, respectively, by [my calculations](https://gist.github.com/jonblatho/003174508c09c2001d38e386a95fe9cd).

### Is there any missing or unavailable data?
* The HCHD did not begin providing an active case count until April 23, 2020. Active cases before that date are estimated by assuming that cases were considered active for 10 days following the report date.
* The HCHD published updates only to its dashboard, which I was unable to archive at the time, for several days in late November 2020. All data is estimated for that period.
* Vaccination data is unavailable prior to December 15, 2020.
* Due to a prolonged and intense winter weather event, the HCHD was closed for several days in mid-February 2021, so testing data is estimated for that period.
* Due to an Internet Archive error, the HCHD dashboard for March 5, 2021, could not be archived, so its source link is unavailable.
* There are two Howell County cases for which, after a thorough review of publicly available data, I have been unable to conclusively identify a corresponding town.

### Why are antigen tests included here?
Many entities do not report COVID-19 antigen tests, but HCHD does. In Howell County, antigen tests have been abnormally common compared to much of the rest of the country. As a result, excluding these tests results the elimination of a significant share of tests and cases. For consistency across datasets, and after carefully considering all variables, I have made the judgment that including antigen tests offers a more realistic picture of the spread of COVID-19 in Howell County.
