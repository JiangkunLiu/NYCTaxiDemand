# NYCTaxiDemand
NYC Taxi data analysis

This project performs taxi demand analysis in NYC, the data were downloaded from http://www.nyc.gov/html/tlc/html/about/trip_record_data.shtml

Data preprocessing

The original data was processed as follows:
1.	Unify column names, as some tables contain capitalized names, and different column names.
2.	Remove outliers, records with missing values, and unreasonable records (very large fare value, negative fare value, passenger number less than 1).
3.	Due to computational limit and time limit, data size was reduced by limiting geometric area of interest, removing records with number of passengers larger than 6.
4.	Obtaining neighborhood name or postcode from geocoding service is very time consuming due to large number of records. To reduce the number of unique coordinates, the latitude and longitude were rounded to 3 decimal digits. To further reduce the unique coordinate number, those coordinates with small number of occurrences (<500 in a month for yellow taxi, and  <100 in a month for green taxi) were removed, and they are not of interest for Via’s business model anyway. Then a lookup table was built for acquiring neighborhood name by coordinates. Those records whose coordinates were not in the lookup table were removed. 
5.	The location lookup table and the cleaned data sets were inner-joined, and then a few features were added, including day, hour, day of week. And the resulting data are ready for analysis.
