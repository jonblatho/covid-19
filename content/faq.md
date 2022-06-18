---
title: Frequently Asked Questions
menu:
  main:
    name: "FAQ"
---

### Where does this data come from?
Most data here came from daily reports published by the Howell County Health Department (HCHD) on their [dashboard](https://archive.ph/Cu8QP) and their [Facebook page](https://www.facebook.com/Howell-County-Health-Department-170310842983730). Vaccination and testing data came from the Missouri Department of Health and Senior Services (DHSS) [vaccine metrics](https://archive.ph/IK6UZ) and [public health metrics](https://archive.ph/mfLxI) pages. Sources corresponding to data, when available, are linked in the [All Data](../all-data) table.

### Why don't daily case counts here match the HCHD dashboard?
Since case data on this dashboard is stored by town and the HCHD only reports the total number of cases per town each day, cases fall under the report date here, while on the HCHD dashboard dates cases correspond to the test date. Usually, the difference is within a few days.

### When is this site updated?
Due to changes in data reporting as of Friday, April 1, 2022, data is no longer updated. All data is frozen as of that date.

### What data is estimated, and how?
When there was a gap in data reporting, such as a weekend, I applied estimates by assuming the number changed linearly between the start and end values across the reporting gap. Estimated data is reflected in the [All Data](../all-data) table with italic text.

Data for active cases by town was estimated by normalizing the 7-day total new cases for the county and categories (cities and “other”) and multiplying the county total active cases by those normalized values. Rounding may cause the sum of the by-town values not to exactly equal the county total. Estimates for active cases by town are hidden when there are few active cases in the county.

### How does data by town work?
Data by town is based on ZIP Code, not city limits. Therefore, for example, while the population of the city of West Plains is about 12,000, its ZIP Code population is actually 24,554 based on 2010 Census data (for the sections of the 65775 ZIP code within Howell County). For Willow Springs and Mountain View, these populations are 5,414 and 5,382, respectively, by [my calculations](https://archive.ph/z65K5).

### Is there any missing or unavailable data?
* The HCHD did not begin providing an active case count until April 23, 2020. Active cases before that date are estimated by assuming that cases were considered active for 10 days following the report date.
* The HCHD published updates only to its dashboard, which I was unable to archive at the time, for several days in late November 2020. All data is estimated for that period.
* Vaccination data is unavailable prior to December 15, 2020.
* Due to an Internet Archive error, the HCHD dashboard for March 5, 2021, could not be archived, so its source link is unavailable.
* There are two Howell County cases for which, after a thorough review of publicly available data, I have been unable to conclusively identify a corresponding town.

### Why are antigen tests included here?
Many entities did not report COVID-19 antigen tests or report them separately, but HCHD combined antigen and PCR tests in their reporting. In Howell County, antigen tests were abnormally common compared to much of the rest of the country. As a result, excluding these tests would have resulted in the elimination of a significant share of tests and cases. Along with consistency concerns between HCHD and DHSS datasets, including antigen tests offered a more realistic picture of the spread of COVID-19 in Howell County.
