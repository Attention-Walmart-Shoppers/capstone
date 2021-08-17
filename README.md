![image](https://user-images.githubusercontent.com/80718340/129650696-3871a9d4-3264-4400-8c8a-1ee6701f7a40.png)

## Project Summary

The goal of this project was to build a sales forecast model that could potentially be used by a regional Wal Mart manager to help manage inventory needs by forecasting consumer demand one week in advance.   We used the data provided by the Kaggle Walmart Recruiting - Store Sales Forecasting challenge which contained weekly sales, holiday flags, temperature, fuel prices, CPI and unemployment by store id and weekly time periods.  After exploring the provided data and identifying potential sales drivers, we utilized the time series data to engineer features we felt would provide a regression model some predictive value.  The biggest challenge in identifying temporal trends that we could leverage in our modeling came when trying to organizing our data in a manner from which we could extract information during the preparation stage.  By varying the lag on our features we were able to overcome the temporal challenges and contructed several regression models that outperformed our benchmark.  Our benchmark was established by using the prior year's weekly_sales data as our forecasts and calculating an RMSE score of 569,729 referencing the actual weekly sales data in our test dataset.  We utilized OLS, LASSOLARS & Polynomial Regression models.  All outperformed the benchmark but our Polynomial model was the best performer with an RMSE score of 292,982.   

|  |Data Dictionary|  |
|Feature|Datatype|Description|
|:-------|:-------|:----------|
|Date|Datetime|weeks ending Friday|
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
