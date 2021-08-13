import pandas as pd 
import numpy as np

def acquire_data():
    '''
    This function creates a Pandas dataframe from 
    walmart stores csv.
    '''
    df = pd.read_csv('walmart_sales.csv')
    df2 = pd.read_csv('stores.csv')
    joined_df  = pd.merge(df,df2,on='Store',how='inner')

    return joined_df

############################ Wrangle Walmart Function ##############################

def wrangle_walmart():
    '''
    This function will bring in the walmart sales csv and cleans it
    then returns a cleaned version as a Pandas dataframe.
    '''
    #return the csv
    df = pd.read_csv('walmart_sales.csv')
    df2 = pd.read_csv('stores.csv')

    #join df together
    joined_df  = pd.merge(df,df2,on='Store',how='inner')

    #change dtype for Date 
    joined_df.Date = joined_df.Date.astype('datetime64[ns]')
    #change dtype for temp
    joined_df.Temperature = joined_df.Temperature.astype(int)
    
    #set date as index and sort
    joined_df = joined_df.set_index('Date').sort_index()

    #change column names
    joined_df = joined_df.rename(columns={"Store": "store", "Weekly_Sales": "weekly_sales", "Holiday_Flag": "holiday_flag", "Temperature": "temperature", "Fuel_Price": "fuel_price", "Unemployment": "unemployment", "Type": "type", "Size": "store_size"})

    #create column to identify month
    joined_df['month'] = joined_df.index.month_name()
    #create column to identify month!
    joined_df['year'] = joined_df.index.year
    #create column for deflating nominal data
    joined_df['deflated_series'] = joined_df.weekly_sales / joined_df.CPI

    #create season column
    joined_df.loc[joined_df['month'] == 'January','season'] ='Winter'
    joined_df.loc[joined_df['month'] == 'February','season'] ='Winter'
    joined_df.loc[joined_df['month'] == 'March','season'] ='Spring'
    joined_df.loc[joined_df['month'] == 'April','season'] ='Spring'
    joined_df.loc[joined_df['month'] == 'May','season'] ='Summer'
    joined_df.loc[joined_df['month'] == 'June','season'] ='Summer'
    joined_df.loc[joined_df['month'] == 'July','season'] ='Summer'
    joined_df.loc[joined_df['month'] == 'August','season'] ='Summer'
    joined_df.loc[joined_df['month'] == 'September','season'] ='Summer'
    joined_df.loc[joined_df['month'] == 'October','season'] ='Fall'
    joined_df.loc[joined_df['month'] == 'November','season'] ='Fall'
    joined_df.loc[joined_df['month'] == 'December','season'] ='Winter'

    #round to 2 decimal places
    joined_df['deflated_series']=joined_df['deflated_series'].apply(lambda x: np.round(x, decimals=2))
    joined_df['fuel_price']=joined_df['fuel_price'].apply(lambda x: np.round(x, decimals=2))
    joined_df['CPI']=joined_df['CPI'].apply(lambda x: np.round(x, decimals=3))

    return joined_df



  