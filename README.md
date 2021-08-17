![image](https://user-images.githubusercontent.com/80718340/129650696-3871a9d4-3264-4400-8c8a-1ee6701f7a40.png)

## Project Summary

The goal of this project was to build a sales forecast model that could potentially be used by a regional Wal Mart manager to help manage inventory needs by forecasting consumer demand one week in advance.   We used the data provided by the Kaggle Walmart Recruiting - Store Sales Forecasting challenge which contained weekly sales, holiday flags, temperature, fuel prices, CPI and unemployment by store id and weekly time periods.  After exploring the provided data and identifying potential sales drivers, we utilized the time series data to engineer features we felt would provide a regression model some predictive value.  The biggest challenge in identifying temporal trends that we could leverage in our modeling came when trying to organizing our data in a manner from which we could extract information during the preparation stage.  By varying the lag on our features we were able to overcome the temporal challenges and contructed several regression models that outperformed our benchmark.  Our benchmark was established by using the prior year's weekly_sales data as our forecasts and calculating an RMSE score of 569,729 referencing the actual weekly sales data in our test dataset.  We utilized OLS, LASSOLARS & Polynomial Regression models.  All outperformed the benchmark but our Polynomial model was the best performer with an RMSE score of 292,982. 

### Project Deliverables:
> Deliver 10 minute presentation walkthrough, and slide presentation communicating to our stakeholders:
- [] the project need and how we attempted to solve it
- [] the assumptions and hypotheses we had going into project
    * how these panned out and evolved throughout the process
- [] how we defined our target variable
- [] how we handled the data and why we made the decisions during preparation we did
- [] our exploratory findings
- [] our modeling results
- [] what methodologies, tools and skills we deployed during the project pipeline
- [] Conclusion, Recommendations & Next Steps

### Data Dictionary:
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

## Stages of DS Pipeline
Plan -> Data Acquisition -> Data Prep -> Exploratory Analysis -> ML Models -> Delivery

### Planning
- [x] Create README.md with data dictionary, project and business goals.
- [x] Acquire data from Kaggle and create a series of functions to automate this process. Save the functions in an new_wrangle.py file to import into the Final Report Notebook.
- [x] Clean and prepare data for the first iteration through the pipeline, MVP preparation. Create a series of functions to automate the process, store the functions in a new_wrangle.py module, and prepare data in Final Report Notebook by importing and using the funtions.
- [x] Establish a baseline accuracy and document.
- [x] Train multiple different regression models on train dataset.
- [x] Evaluate models on test dataset.
- [] Document conclusions, takeaways, and next steps in the Final Report Notebook.

### Data Acquistion
- [X] Download Kaggle Walmart Sales Forecasting datasets: walmart_sales.csv & stores.csv
- [x] read both .csv files into a pandas dataframe and merge 
- [x] Automate this process in a single function and save to new_wrangle.py
- [x] The final function will return a merged pandas DataFrame.
- [] Import the acquire function from the new_wrangle.py module and use it to acquire the data in the Final Report Notebook.
- [x] Complete some initial data summarization (`.info()`, `.describe()`, `.value_counts()`, `.nunique()`, ...).

### Data Preparation
- [x] After initial exploration, perform an initial prep that includes:
    * addressing null or missing values
    * rename and lower case column labels
    * address dtypes and perform necessary conversions
    * round floats to two decimals
- [x] address outliers and save function in new_wrangle.py
- [x] create new season feature and save function in new_wrangle.py
- [x] create new features and save function in new_wrangle.py
- [x] create dummy variables for holiday_name and save function in new_wrangle.py
- [x] create column detailing holilday name and save function in new_wrangle.py
- [x] create a single master function that combines and applies the previous functions to our raw dataframe and save function in new_wrangle.py
- [x] Scale numeric data, concat with object dataframe and save function in new_wrangle.py 
- [x] Split data into train, test, X_train, y_train, X_test and y_test sets and save function in new_wrangle.py
- [x] Combine the scale and split function into one split_scale() function
- [x] Document Key Findings & Takeaways, as well as possible routes to take after MVP / First Iteration

### Exploratory Analysis
- []  
- [] Summarize our conclusions, provide clear answers to our specific questions, and summarize any takeaways/action plan from the work above.
- [] Document further data preparation steps to be looked into after MVP / first iteration through the DS pipeline

## ML Models
- [x] Construct and evaluate:
    * Ordinary Least Squares (OLS), LASSO LARS & Polynomial Regression models
- [x] Establish two baselines 
    * the first, by averaging our weekly_sales data in our train dataset and using this mean as our forecasted values to evaluate against our actual weekly_sales data in our test dataset to calculate a RMSE baseline
    * the second, using the prior year's weekly_sales data as our forecasted values to evaluate against our actual weekly_sales data in our test dataset to calculate a RMSE baseline
- [x] Train (fit, transform, evaluate) the models, varying the algorithm and/or hyperparameters we use.
- [x] Compare RMSE metrics across all models and evaluate against our baseline RMSE.
- [] Feature Selection (after initial iteration through pipeline): Are there any variables that seem to provide limited to no additional information?  Are there any alternative feature selection processes that could improve results

## Conclusions & Next Steps

- 