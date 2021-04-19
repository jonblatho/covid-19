---
title: Notes
menu: main
---

### Methodology
* Most data here comes directly from daily reports by the Howell County Health Department. Sometimes, there are gaps in reporting due to holidays, inclement weather, or other reasons. To fill in these gaps, I apply a linear equation to estimate the missing data. Where sources are available, those are linked in the [All Data](../all-data) table.
* Testing data is published on weekday mornings only, with Monday updates reflecting testing for the preceding weekend and other days reflecting the prior day's testing. Absent testing data, I estimate testing numbers by assuming that the 14-day positivity rate is the same until reporting resumes. Sometimes this isn't mathematically possible --- that is, tests would have to be subtracted in order to maintain the positivity rate --- in which case I keep the positivity rate as close as possible to the last known value.
* While HCHD reports the total active cases for the county, data for active cases by town is estimated. This is done by normalizing the 7-day total new cases for the county and categories (cities and “other”) and multiplying the county total active cases by those normalized values. Rounding may cause the sum of the by-town values not to exactly equal the county total. Estimates for active cases by town are hidden when there are fewer than 10 active cases in the county.

### Notes
* Data by town is based on ZIP code. Therefore, for example, while the population of the city of West Plains is about 12,000, its ZIP code population is actually 24,554 based on 2010 Census data (for the sections of the 65775 ZIP code within Howell County). For Willow Springs and Mountain View, these populations are 5,414 and 5,382, respectively, by [my calculations](https://gist.github.com/jonblatho/003174508c09c2001d38e386a95fe9cd).
* HCHD did not begin providing an active case count until April 23, 2020. Active cases before then are estimated by assuming that cases were considered active for 10 days following the report date.
* Due to an Internet Archive error, the HCHD dashboard for March 5, 2021, could not be archived, so its source link is unavailable.
* This page includes both official data and unofficial estimates. For official data, please consult the Howell County Health Department.

### Update Schedule
* **Evening updates:** Most data is updated automatically around 11 PM each night. Cases are not added on Sundays. Testing data is not available until the morning (on weekdays only), so testing numbers are estimated in the evening updates.
* **Morning updates:** In the morning each weekday, the evening updates are amended to include actual test counts (when available), which must be added manually.