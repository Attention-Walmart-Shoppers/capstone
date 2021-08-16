import pandas as pd 
import numpy as np

import datetime as dt 

##################### ACQUIRE WALMART DATA #####################

def acquire_data():
    '''
    This function creates a Pandas dataframe from 
    walmart stores csv and sets the index as Date.
    '''
    df = pd.read_csv('walmart_sales.csv')
    df2 = pd.read_csv('stores.csv')
    joined_df  = pd.merge(df,df2,on='Store',how='inner')

    return joined_df


############################ Change Dtypes and Names Function ##############################

def change_columns(df):
    '''
    This function changes column names, dtypes and rounds decimal places
    then returns a cleaned dataframe
    '''
    #change dtype for Date 
    df.Date = pd.to_datetime(df.Date, dayfirst=True)

    #change column names
    df = df.rename(columns={"Store": "store_id", "Weekly_Sales": "weekly_sales", "Holiday_Flag": "holiday_flag", "Temperature": "temperature", "Fuel_Price": "fuel_price", "Unemployment": "unemployment", "Type": "store_type", "Size": "store_size"})

    #change dtype for temp
    df.temperature = df.temperature.astype(int)
    #dtype into string
    df['store_id'] = df['store_id'].astype(str)


    #round to 2 decimal places
    df['fuel_price']=df['fuel_price'].apply(lambda x: np.round(x, decimals=2))
    df['CPI']=df['CPI'].apply(lambda x: np.round(x, decimals=3))

    return df


############################ New Features Function ##############################

def new_features(df):
    '''
    This function creates several new columns
    and returns the completed dataframe
    '''
    #create column to identify month
    df['month'] = pd.DatetimeIndex(df['Date']).month_name()
    #create column to identify month!
    df['year'] = pd.DatetimeIndex(df['Date']).year
    #create column to identify month!
    df['quarter'] = pd.DatetimeIndex(df['Date']).quarter
    #day of week
    df['weekday'] = pd.DatetimeIndex(df['Date']).day_name()
    #create column for week of the year
    df['week_of_year'] = pd.DatetimeIndex(df['Date']).week

    #create column for deflating nominal data
    df['deflated_series'] = df.weekly_sales / df.CPI
    #change to 2 decimal places
    df['deflated_series']=df['deflated_series'].apply(lambda x: np.round(x, decimals=2))

    #change in sales by week
    df['sales_delta_weekly'] = df.groupby('store_id').weekly_sales.diff(periods=1)
    #change in sales by year
    df['sales_delta_yearly'] = df.groupby('store_id').weekly_sales.diff(periods=52)
    #change in gas prices by week
    df['gas_delta_weekly'] = df.groupby('store_id').fuel_price.diff(periods=1)
    #change in gas prices by year
    df['gas_delta_yearly'] = df.groupby('store_id').fuel_price.diff(periods=52)
    #sales from last year
    df['last_year_sales'] = df.groupby('store_id').weekly_sales.shift(-52)
    #sales for last week
    df['last_week_sales'] = df.groupby('store_id').weekly_sales.shift(-1)
    
    #new column pre_christmas and add zeros
    df ['pre_christmas'] = 0
    #getting the list for pre_christmas
    pre_c= ['2010-12-24', '2010-12-17', '2011-12-23', '2011-12-16']
    #add value 1 for only pre_christmas weeks
    df.loc[pre_c, 'pre_christmas'] = 1

    #ADD TAX SEASON
    df2['tax_season'] = 0 
    #getting the list for tax
    tax= ['2010-04-02 ', '2010-04-09', '2011-04-01', '2011-04-08', '2012-04-06', '2012-04-13']
    #add value 1 for only for the list above
    df.loc[tax, 'tax_season'] = 1

    #fill delta nulls with 0
    df['sales_delta_weekly'] = df['sales_delta_weekly'].fillna(0)
    df['gas_delta_weekly'] = df['gas_delta_weekly'].fillna(0)
    df['sales_delta_yearly'] = df['sales_delta_yearly'].fillna(0)
    df['gas_delta_yearly'] = df['gas_delta_yearly'].fillna(0)

    #set date as index and sort
    df = df.set_index('Date').sort_index()

    return df


############################ Seasons Function ##############################

def season_column(df):
    '''
    This function creates a new column called season
    using the month column
    '''
    #create season column
    df.loc[df['month'] == 'January','season'] ='Winter'
    df.loc[df['month'] == 'February','season'] ='Winter'
    df.loc[df['month'] == 'March','season'] ='Spring'
    df.loc[df['month'] == 'April','season'] ='Spring'
    df.loc[df['month'] == 'May','season'] ='Summer'
    df.loc[df['month'] == 'June','season'] ='Summer'
    df.loc[df['month'] == 'July','season'] ='Summer'
    df.loc[df['month'] == 'August','season'] ='Summer'
    df.loc[df['month'] == 'September','season'] ='Summer'
    df.loc[df['month'] == 'October','season'] ='Fall'
    df.loc[df['month'] == 'November','season'] ='Fall'
    df.loc[df['month'] == 'December','season'] ='Winter'

    return df

########################### Address Outliers Function ###########################


def address_outliers(df):
    '''
    This function addresses outliers with store type
    and it change the store type to be corrected
    '''
    df[df['store_id'] ==3] = df.loc[df['store_id'] == 3].replace({'B':'C'})
    df[df['store_id'] ==5] = df.loc[df['store_id'] == 5].replace({'B':'C'})
    df[df['store_id'] ==33] = df.loc[df['store_id'] == 33].replace({'A':'C'})
    df[df['store_id'] ==36] = df.loc[df['store_id'] == 36].replace({'A':'C'})

    return df


########################### Create dummy Variables Function ###########################

def create_dummies (df, dumm_col = ['holiday_name']):
    '''
    Takes in a df and columns to create dummies.
    retunr the original df with de new columns (dummies)
    '''
    #create dummy variables 
    for col in dumm_col:
        #create dummies
        df_dummies = pd.get_dummies(df[col], dummy_na=False)
        #  concat df_dummies with my df
        df = pd.concat([df, df_dummies], axis =1)
    #drop no_holiday columns and year
    df = df.drop(columns = ['no_holiday'])
    return df

############################ Wrangle Walmart Function ##############################

def wrangle_walmart():
    '''
    This function will bring in the walmart sales csv and cleans it
    then returns a cleaned version as a Pandas dataframe.
    '''
    
    # acquire data
    df = acquire_data()
    
    # change columns
    df = change_columns(df)

    # new columns
    df = new_features(df)

    # season column
    df = season_column(df)
    
    # holiday column
    df = add_which_holiday(df)

    #address outliers
    df = address_outliers(df)

    #create dummies
    df = create_dummies (df)

    return df

############################ SPLIT FUNCTION ##############################

def train_test(df, target):
    '''
    This function brings in the dataframe and the target feature
    then returns X_train, y_train, X_test and y_test with their respective shapes
    '''
    train = df[:'05-2012'] # includes everything until june 2016
    test = df['06-2012':"2012"] #includes last 6 months

    # split train into X (dataframe, drop target) & y (series, keep target only)
    X_train = train.drop(columns=[target])
    y_train = train[target]

    # split test into X (dataframe, drop target) & y (series, keep target only)
    X_test = test.drop(columns=[target])
    y_test = test[target]

    # Have function print datasets shape
    print(f'X_train -> {X_train.shape}')
    print(f'X_test -> {X_test.shape}')
    print(f'train -> {train.shape}')
    print(f'test -> {test.shape}')

    return train, test, X_train, y_train, X_test, y_test

############################ WHICH HOLIDAY FUNCTION ##############################

def add_which_holiday(df):
    '''
    This function takes in the walmart dataframe
    Has list of different dates for holidays in the function
    Adds a column called 'holiday_name' with the name of the holiday if that week corresponds
    with the date
    any that don't have a holiday get filled with the value no_holiday
    
    '''
    # create lists of holidays 
    christmases = ['2010-12-31', '2011-12-30', '2012-12-28']

    super_bowls = ['2010-02-12', '2011-02-11', '2012-02-10']

    labor_days = ['2010-09-10', '2011-09-09', '2012-09-07']

    thanksgivings = ['2010-11-26', '2011-11-25', '2012-11-23']
    
    # turn christmas list into datetimes 
    dates_list = [dt.datetime.strptime(date, "%Y-%m-%d").date() for date in christmases]
    # add column called holiday_name christmas where dates match list
    df.loc[df.index.isin(dates_list) == True, 'holiday_name'] = 'christmas'
    
    # turn super bowl list into date times
    dates_list = [dt.datetime.strptime(date, "%Y-%m-%d").date() for date in super_bowls]  
    #add super bowl where dates match list
    df.loc[df.index.isin(dates_list) == True,'holiday_name'] = 'super_bowl'
    
    # labor day list into date times
    dates_list = [dt.datetime.strptime(date, "%Y-%m-%d").date() for date in labor_days] 
    # add super bowl where dates match list
    df.loc[df.index.isin(dates_list) == True, 'holiday_name'] = 'labor_day'
    
    # thanksgiving list into date times
    dates_list = [dt.datetime.strptime(date, "%Y-%m-%d").date() for date in thanksgivings] 
    # add super bowl where dates match list
    df.loc[df.index.isin(dates_list) == True, 'holiday_name'] = 'thanksgiving'
    
    df = df.fillna('no_holiday')
    
    return df

############################ Scale  ##############################
def scaled_df ( train_df , test_df, columns,  scaler):
    '''
    Take in a 3 df and a type of scaler that you  want to  use. it will scale all columns
    except object type. Fit a scaler only in train and tramnsform in train, validate and test.
    returns  new dfs with the scaled columns.
    scaler : MinMaxScaler() or RobustScaler(), StandardScaler() 
    Example:
    scaled_df( X_train , X_test, columns , RobustScaler())
    
    '''
    #import
    from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler
    # fit our scaler
    scaler.fit(train_df[columns])
    # get our scaled arrays
    train_scaled = scaler.transform(train_df[columns])
    test_scaled= scaler.transform(test_df[columns])

    # convert arrays to dataframes
    train_scaled_df = pd.DataFrame(train_scaled, columns=columns).set_index([train_df.index.values])
    test_scaled_df = pd.DataFrame(test_scaled, columns=columns).set_index([test_df.index.values])

    #add the columns that are not scaled
    train_scaled_df = pd.concat([train_scaled_df, train_df.drop(columns = columns) ], axis= 1 )
    test_scaled_df = pd.concat([test_scaled_df, test_df.drop(columns = columns) ], axis= 1 )
    #plot
    for col in columns: 
        plt.figure(figsize=(13, 6))
        plt.subplot(121)
        plt.hist(train_df[col], ec='black')
        plt.title('Original')
        plt.xlabel(col)
        plt.ylabel("counts")
        plt.subplot(122)
        plt.hist(train_scaled_df[col],  ec='black')
        plt.title('Scaled')
        plt.xlabel(col)
        plt.ylabel("counts")



    return train_scaled_df,  test_scaled_df