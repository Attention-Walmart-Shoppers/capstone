![image](https://user-images.githubusercontent.com/80718340/129650696-3871a9d4-3264-4400-8c8a-1ee6701f7a40.png)

## Project Summary

The goal of this project was to utilize 

||Data Dictionary||
|Feature|Datatype|Description|
|:-------|:-------|:----------|
|Date|Datetime|week ending Friday|
|store_id|int64|unique store identifier (45 stores)|
|weekly_sales |float64|sales for the given store|
|holiday_flag|int64|boolean indicator of holiday week. Holidays inlcude: SuperBowl, Labor Day, Thanksgiving/Black Friday & Christmas|
|temperature|int64 |temperature in Farenheit on Date of sale|
|fuel_price|float64|cost of fuel in the region|
|CPI|float64|prevailing consumer price index|
|Unemployment|float64|prevailing unemployment rate|
|store_type|object|three undefined but labeled store types|
|store_size|int64|size by square feet|
|holiday_name|object|name of flagged holiday period|
|month|object|month during which Date occurs|
|year|int64|year during which Date occurs|
|quarter|int64|integer representing calendar quarter during which Date occurs|
|weekday|object|weekday on which Date falls|
|deflated_series|float64|weekly_sales delfated bye CPI|
|sales_delta_weekly|float64|weekly difference in weekly_sales by store_id|
|sales_delta_yearly|float64|yearly difference in weekly_sales by store_id|
|gas_delta_weekly|float64|weekly difference in fuel_price by store_id|
|gas_delta_yearly|float64|yearly difference in fuel_price by store_id|
|last_year_sales|float64|weekly sales for same store_id one year prior|
|last_week_sales|float64|weekly sales for same store_id one week prior|
|pre_christmas|int64|two weeks prior to Christmas holiday flag|
|tax_season|int64|first two weeks in April|
|season|object|season during which Date occurs: Winter, Spring, Summer, Fall|
