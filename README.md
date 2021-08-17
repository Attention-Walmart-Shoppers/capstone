![image](https://user-images.githubusercontent.com/80718340/129650696-3871a9d4-3264-4400-8c8a-1ee6701f7a40.png)

## Project Summary

The goal of this project was to utilize 

|Feature|Datatype|Description|
|:-------|:-------|:----------|
|Store|int64|unique store identifier (45 stores)|
|Date|object|the original contents of the README file|
|cleaned_readme_contents|object|the contents of the README file after going through 'basic_clean' function|
|stemmed_readme_contents|object|the contents of the README file after going through 'basic_clean' and 'stem' functions|
|lemmatized_readme_contents|object|the contents of the README file after going through 'basic_clean' and 'lemmatize' functions|

Store	int64	unique identifier for store (1-45)
Date	object	Date of transaction
Holiday_Flag	int64	indicator of a Holiday week (boolean)
Temperature	float64	temperature in Farenheight
Fuel_Price	float64	cost of fuel(in USD) in region
CPI	float64	Prevailing consumer price index, cost of goods
Unemployment	float64	Prevailing unemployment rate

 #   Column  | Datatype | Description |
---  ------  | -------- | ----------- | 
 0   store_id | object  | Unique store identifier (45 stores) |
 
 
 1   weekly_sales        6435 non-null   float64
 2   holiday_flag        6435 non-null   int64  
 3   temperature         6435 non-null   int64  
 4   fuel_price          6435 non-null   float64
 5   CPI                 6435 non-null   float64
 6   unemployment        6435 non-null   float64
 7   store_type          6435 non-null   object 
 8   store_size          6435 non-null   int64  
 9   holiday_name        6435 non-null   object 
 10  month               6435 non-null   object 
 11  year                6435 non-null   int64  
 12  quarter             6435 non-null   int64  
 13  weekday             6435 non-null   object 
 14  week_of_year        6435 non-null   int64  
 15  deflated_series     6435 non-null   float64
 16  sales_delta_weekly  6435 non-null   float64
 17  sales_delta_yearly  6435 non-null   float64
 18  gas_delta_weekly    6435 non-null   float64
 19  gas_delta_yearly    6435 non-null   float64
 20  last_year_sales     4095 non-null   float64
 21  last_week_sales     6390 non-null   float64
 22  pre_christmas       6435 non-null   int64  
 23  tax_season          6435 non-null   int64  
 24  season              6435 non-null   object 