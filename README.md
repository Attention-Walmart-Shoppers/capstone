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

### -  Initial Data

| Feature          | Datatype | Description                                                                                                      |
|------------------|----------|------------------------------------------------------------------------------------------------------------------|
| `Store`          | int64    | Unique store identifier (45 stores)                                                                              |
| `Date`           | object   | Weeks ending Friday                                                                                              |
|  `Weekly_Sales`  | float64  | Sales for the given store                                                                                        |
| `Holiday_Flag`   | int64    | Boolean indicator of holiday week. Holidays include: SuperBowl, Labor Day, Thanksgiving/Black Friday & Christmas |
| `Temperature`    | float64  | Temperature in Farenheit on Date of sale                                                                         |
| `Fuel_Price`     | float64  | Cost of fuel in the region                                                                                       |
| `CPI`            | float64  | Prevailing consumer price index                                                                                  |
| `Unemployment`   | float64  | Prevailing unemployment rate                                                                                     |
| `Type`           | float64  | Three  types of stores  by size : A (large ) , B (medium), C (small)                                             |
| `Size`           | int64    | Size by square feet                                                                                              |

### - Final

| Feature                   | Datatype       | Description                                                                                                      |
|---------------------------|----------------|------------------------------------------------------------------------------------------------------------------|
| `store_id`                | object         | Unique store identifier (45 stores)                                                                              |
| `this_week_date           | datetime64[ns] | Date of the current week ending Friday                                                                           |
|  `this_week_sales`        | float64        | Week sales for the given store                                                                                   |
| `this_week_holiday_flag`  | int64          | Boolean indicator of holiday week. Holidays include: SuperBowl, Labor Day, Thanksgiving/Black Friday & Christmas |
| `temperature`             | float64        | Temperature in Farenheit on Date of sale                                                                         |
| `fuel_price`              | float64        | Cost of fuel in the region                                                                                       |
| `CPI`                     | float64        | Prevailing consumer price index                                                                                  |
| `this_week_unemployment`  | float64        | Prevailing unemployment rate                                                                                     |
| `store_type`              | float64        | Three  types of stores  by size : A (large ) , B (medium), C (small)                                             |
| `store_size`              | int64          | Size by square feet                                                                                              |
| `next_week_1_year_ago`    | float64        | Weekly sales 51 weeks ago                                                                                        |
| `next_week_date`          | datetime64[ns] | Date of the next week                                                                                            |
| `next_week_holiday_flag`  | float64        | Boolean indicator of holliday next week                                                                          |
| 'this_week_season'        | object         | Season during next week occurs :Winter, Spring, Summer, Fall                                                     |
| 'this_week_season'        | object         | Season during next week occurs :Winter, Spring, Summer, Fall                                                     |
| `next_week_holiday_name`  | object         | Holiday name of the next week                                                                                    |
| `christmas`               | uint8          | Christmas holiday flag based on next week                                                                        |
| `labor_day`               | uint8          | Pre-Christmas holiday flag based on next week                                                                    |
| `labor_day`               | uint8          | Pre-Christmas holiday flag based on next week                                                                    |
| `superbowl`               | uint8          | Superbowl holiday flag based on next week                                                                        |
| `thanksgiving`            | unit8          | Thanksgiving holiday flag based on next week                                                                     |
| `fuel_4wk_rolling`        | float64        |     (US dollar)                                                                                                             |
| `cpi_4wk_rolling`         | float64        |                                                                                                                  |
| `unemp_4wk_rolling`       | float64        |                                                                                                                  |
| `avgMoM_perc_fuel`        | float64        |                                                                                                                  |
| `avgMoM_perc_unemp`       | float64        |                                                                                                                  |
| `fuel_quarterly_rolling`  | float64        |                                                                                                                  |
| `cpi_quarterly_rolling`   | float64        |                                                                                                                  |
| `unemp_quarterly_rolling` | float64        |                                                                                                                  |
| `avgQoQ_perc_fuel`        | float64        |                                                                                                                  |
| `avgQoQ_perc_cpi`         | float64        |                                                                                                                  |
| `avgQoQ_perc_unemp`       | float64        |                                                                                                                  |

#### Target
| Feature                   | Datatype       | Description                                                                                                      |
|---------------------------|----------------|------------------------------------------------------------------------------------------------------------------|
| `next_week_sales_target`                | float64        | prediction (next week sales ) US dollar

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