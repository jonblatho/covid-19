# COVID-19 in Howell County, Missouri
**Note:** Due to data reporting changes, daily updates for this project were suspended following the Friday, April 1, 2022, update. Data will remain frozen as of that date, but the project and its source code will remain available indefinitely.

----

This repository contains the daily data files used to generate my [COVID-19 dashboard](https://covid.jonblatho.com/) for Howell County, Missouri, as well as the [Hugo](https://gohugo.io/) source files needed to generate the page, and the Python source files for processing and updating the daily data files.

## How it works
1. Daily data is entered into the relevant file in the daily-data directory.
2. Python scripts process the daily data into files for the dashboard.
3. [Hugo](https://gohugo.io/) uses these data files and template files to generate HTML.
4. The generated HTML is deployed to AWS.

## Notable updates

* **October 25, 2020:** Launched the dashboard site at https://covid.jonblatho.com/.
* **October 26, 2020:** Added a table with all daily data.
* **October 27, 2020:** The total cases chart was changed from a single line for total cases in the county to a stacked area chart with data by town.
* **November 8, 2020:** Added vertical markers on the total cases chart to show dates of significant events.
* **November 9, 2020:** Changed the positivity rate metric from the 7-day positivity rate to the 14-day positivity rate.
* **November 24, 2020:** Added a column in the table to show the discrepancy between HCHD and DHSS reported case totals for a given date.
* **December 8, 2020:** Date markers on the dashboard chart can now be toggled on and off.
* **December 9, 2020:** Added charts for new cases, active cases, and positivity rate.
* **December 18, 2020:** Moved the All Data table to its own page and added Dark Mode support.
* **January 5, 2021:** Added a categorical risk level to characterize the status of COVID-19 in the county.
* **January 21, 2021:** Added historical risk levels to the All Data table.
* **January 31, 2021:** Open-sourced Python processing script.
* **February 10, 2021:** Automated nightly updates at 11 PM and 12 AM CST.
* **March 25, 2021:** Made site responsive to improve legibility on mobile devices.
* **July 4, 2021:** Added two vaccination charts to the homepage.
* **July 9, 2021:** Redesigned the chart and dashboard section of the homepage with a new full-width layout.
* **August 1, 2021:** Redesigned the Active Cases by Town section as a map with estimates available for all Howell County towns.
* **August 10, 2021:** Adds a customized calculation of the CDC Level of Community Transmission parameter including antigen tests, which are anomalously common in Howell County.
* **August 12, 2021:** Redesigned and expanded All Data table with support for new cases by town for all towns, vaccination data, and a new CDC Level of Community Transmission column.
* **September 13, 2021:** Migrated the site from GitHub Pages to AWS using S3 and CloudFront.
* **October 3, 2021:** Added an automation to pull in state DHSS data daily.
* **October 6, 2021:** Monthly case tables were split up by year in an accordion format, with the current year expanded and past year(s) collapsed by default.
* **April 1, 2022**: Final regular data update due to data reporting changes.