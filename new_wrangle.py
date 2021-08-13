import pandas as pd 
import numpy as np

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

def change_columns():
    '''
    This function changes column names, dtypes and rounds decimal places
    then returns a cleaned dataframe
    '''
    #acquire data
    df= acquire_data()

    #change dtype for Date 
    df.Date = df.Date.astype('datetime64[ns]')

    #change column names
    df = df.rename(columns={"Store": "store_id", "Weekly_Sales": "weekly_sales", "Holiday_Flag": "holiday_flag", "Temperature": "temperature", "Fuel_Price": "fuel_price", "Unemployment": "unemployment", "Type": "type", "Size": "store_size"})

    #change dtype for temp
    df.temperature = df.temperature.astype(int)
    
    #round to 2 decimal places
    df['fuel_price']=df['fuel_price'].apply(lambda x: np.round(x, decimals=2))
    df['CPI']=df['CPI'].apply(lambda x: np.round(x, decimals=3))

    return df


############################ New Features Function ##############################

def new_features():
    '''
    This function creates several new columns
    and returns the completed dataframe
    '''
    #acquire change column function
    df = change_columns()

    #create column to identify month
    df['month'] = pd.DatetimeIndex(df['Date']).month_name()
    #create column to identify month!
    df['year'] = pd.DatetimeIndex(df['Date']).year
    #create column to identify month!
    df['quarter'] = pd.DatetimeIndex(df['Date']).quarter

    #create column for deflating nominal data
    df['deflated_series'] = df.weekly_sales / df.CPI
    #change to 2 decimal places
    df['deflated_series']=df['deflated_series'].apply(lambda x: np.round(x, decimals=2))

    #change in sales by week
    df['sales_delta'] = df.groupby('store_id').weekly_sales.diff(periods=1)

    #set date as index and sort
    df = df.set_index('Date').sort_index()

    return df


############################ Seasons Function ##############################

def season_column():
    '''
    This function creates a new column called season
    using the month column
    '''
    #acquire the new features function
    df = new_features()

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


############################ Wrangle Walmart Function ##############################

def wrangle_walmart():
    '''
    This function will bring in the walmart sales csv and cleans it
    then returns a cleaned version as a Pandas dataframe.
    '''
    
    # acquire data
    df = acquire_data()
    
    # change columns
    df = change_columns()

    # new columns
    df = new_features()

    # season column
    df = season_column()

    return df



  