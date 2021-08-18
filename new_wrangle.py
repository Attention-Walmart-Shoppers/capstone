import pandas as pd 
import numpy as np
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings("ignore")
from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler
import datetime as dt 
import matplotlib.pyplot as plt

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
    df['deflated_series'] = df.weekly_sales / df.inflation
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


    #fill delta nulls with 0
    df['sales_delta_weekly'] = df['sales_delta_weekly'].fillna(0)
    df['gas_delta_weekly'] = df['gas_delta_weekly'].fillna(0)
    df['sales_delta_yearly'] = df['sales_delta_yearly'].fillna(0)
    df['gas_delta_yearly'] = df['gas_delta_yearly'].fillna(0)

    #set date as index and sort
    df = df.set_index('Date').sort_index()


    return df

########################### The this week/next week function #####################

def this_week_next_week_lagger(df):
    '''
    This function creates the lags for next week
    And renames the date column to this_week
    '''
    # rename columns for clarity with this week
    df = df.rename(columns = {'weekly_sales': 'this_week_sales',
                                'Date': 'this_week_date',
                                'holiday_flag': 'this_week_holiday_flag', 
                                'unemployment':'this_week_unemployment'})

    #Get data for the prediction week from one year ago
    df['next_week_1_year_ago'] = df.groupby('store_id').this_week_sales.shift(51)

    # get next week data TARGET CREATION
    df['next_week_sales_target'] = df.groupby('store_id').this_week_sales.shift(-1)

    #create column showing the next_week's date
    df['next_week_date'] = df.groupby('store_id').this_week_date.shift(-1)

    # get whether next week is a holiday or not
    df['next_week_holiday_flag'] = df.groupby('store_id').this_week_holiday_flag.shift(-1)

    return df    

############################ Seasons Function ##############################
def get_season(now_date):
    '''
    This function gets the season from a dateteime
    '''
    
    Y = 2000 # dummy leap year to allow input X-02-29 (leap day)
    seasons = [('winter', (date(Y,  1,  1),  date(Y,  3, 20))),
           ('spring', (date(Y,  3, 21),  date(Y,  6, 20))),
           ('summer', (date(Y,  6, 21),  date(Y,  9, 22))),
           ('fall', (date(Y,  9, 23),  date(Y, 12, 20))),
           ('winter', (date(Y, 12, 21),  date(Y, 12, 31)))]
        
    now = now_date.replace(year=Y)
    
    season = next(season for season, (start, end) in seasons if start <= now <= end)
    
    return season


def season_column(df):
    '''
    This function creates two new columns 
    Season for this week date 
    And season for next week date
    Uses get_season function
    '''

    df['next_week_season'] = df.dropna().next_week_date.apply(get_season)

    df['this_week_season'] = df.dropna().this_week_date.apply(get_season)

    return df

########################### Address Outliers Function ###########################


def address_outliers(df):
    '''
    This function addresses outliers with store type
    and it change the store type to be corrected
    '''
    df[df['store_id'] =='3'] = df.loc[df['store_id'] == '3'].replace({'B':'C'})
    df[df['store_id'] =='5'] = df.loc[df['store_id'] == '5'].replace({'B':'C'})
    df[df['store_id'] =='33'] = df.loc[df['store_id'] == '33'].replace({'A':'C'})
    df[df['store_id'] =='36'] = df.loc[df['store_id'] == '36'].replace({'A':'C'})

    return df


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

    pre_c= ['2010-12-24', '2010-12-17', '2011-12-23', '2011-12-16']

    tax= ['2010-04-02 ', '2010-04-09', '2011-04-01', '2011-04-08', '2012-04-06', '2012-04-13']

    # add column called holiday_name christmas where dates match list
    df.loc[df['next_week_date'].isin(christmases) == True, 'next_week_holiday_name'] = 'christmas'
      
    #add super bowl where dates match list
    df.loc[df['next_week_date'].isin(super_bowls) == True,'next_week_holiday_name'] = 'super_bowl'
    
    # add super bowl where dates match list
    df.loc[df['next_week_date'].isin(labor_days) == True, 'next_week_holiday_name'] = 'labor_day'
    
    # add super bowl where dates match list
    df.loc[df['next_week_date'].isin(thanksgivings) == True, 'next_week_holiday_name'] = 'thanksgiving'

    #add pre_christmas
    df.loc[df['next_week_date'].isin(pre_c)==True, 'next_week_holiday_name'] = 'pre_christmas'
    
    # fill the rest with string no_holiday
    df['next_week_holiday_name'] = df['next_week_holiday_name'].fillna('no_holiday')
    
    df['next_week_date'] = pd.to_datetime(df.next_week_date, dayfirst=True)
    
    return df

########################### Create dummy Variables Function ###########################

def create_dummies (df, dumm_col = ['next_week_holiday_name']):
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

################## New Index Function ########################

def get_new_index(df):
    '''
    This function takes in the walmart dataframe
    Resets the index
    Calculates a new field from this_week_date and next_week_date and store_id
    and set's that as the index
    '''
    # create new index from the 
    # this_week_store_1_next_week
    df['id'] = df['this_week_date'].dt.date.astype(str) + '_store_'+ df['store_id'] +'_' + df['next_week_date'].dt.date.astype(str)

    # set id column as the new index
    df = df.set_index('id')

    return df

############################ Drop Columns Function ############################

def column_dropper(df):
    '''
    This function drops the columns we won't be using 
    '''

    df = df.drop(columns = ['temperature'])

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

    #do all the this week that week laging stuff
    df = this_week_next_week_lagger(df)

    # add seasons columns
    df = season_column(df)
    
    # holiday column
    df = add_which_holiday(df)

    # address outliers
    df = address_outliers(df)

    # create dummies
    df = create_dummies(df)

    # create new identifier index 
    df = get_new_index(df)

    # drop unneeded columns
    df = column_dropper(df)

    return df

############################ SPLIT FUNCTION ##############################

def train_test(df, target):
    '''
    This function brings in the dataframe and the target feature
    then returns X_train, y_train, X_test and y_test with their respective shapes
    '''
    # split df into test (20%) and train_validate (80%)
    train, test = train_test_split(df, test_size=0.3, random_state=123)

    # split train into X (dataframe, drop target) & y (series, keep target only)
    X_train = train.drop(columns=[target])
    y_train = train[target]

    # split test into X (dataframe, drop target) & y (series, keep target only)
    X_test = test.drop(columns=[target])
    y_test = test[target]

    # Have function print datasets shape
    print(f'train -> {train.shape}')
    print(f'test -> {test.shape}')

    return train, test, X_train, y_train, X_test, y_test




############################ Scale  ##############################
def scaled_df ( train_df , test_df, columns,  scaler, graphs = True):
    '''
    Take in a 3 df and a type of scaler that you  want to  use. it will scale all columns
    except object type. Fit a scaler only in train and tramnsform in train, validate and test.
    if graphs = True, will show distributions
    To turn off graphs set graphs = False
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


    if graphs == True:
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


#################### Split & Scale Function #########################

def split_scale (df, target, scaler = None):
    ''' 
    This function takes in a dataframe
    A Target variable
    And An optional argument Scaler (i.e. MinMaxScaler())
    If there is no Scaler argument: Function drops nulls, 
    Resets index, and splits in to train and test (ONLY RETURNS 2 THINGS)
    ---
    train, test = split_scale(df, target)
    
    ~~~~~~~~~

    If there is a scaler argument: function drops nulls, 
    resets index, scales only numeric columns,
    splits into, train, test, and further 
    into X_train_scaled, X_test_scaled, y_train, y_test
    (RETURNS 6 THINGS) 
    ---
    train, test, X_train_scaled, X_test_scaled, y_train, y_test = split_scale(df, target, scaler = MinMaxScaler())
    '''
    # Drop NaNs from creating new features (first year of data)
    df = df.dropna()
    
    # Create new index from store ID and date 
    df = get_new_index(df)
    
    # If no scaler argument input, only splits train and test (for exploration)
    if scaler == None:
        # split df into test (20%) and train_validate (80%)
        train, test = train_test_split(df, test_size=0.3, random_state=123)
        # Have function print datasets shape
        print(f'train -> {train.shape}')
        print(f'test -> {test.shape}')
        # return only train and test
        return train, test
       
    # if scaler argument is present, further splits into Xy dataframes
    else:
        # Turn Datetime back into object
        df = df.drop(columns = ['next_week_date', 'this_week_date'])
        
        #split using train test split function above
        train, test, X_train, y_train, X_test, y_test = train_test(df, target)
        
        #select the columns to scale
        columns =  X_train.select_dtypes(exclude='object').columns.to_list()
        
        #scale 
        X_train_scaled, X_test_scaled = scaled_df( X_train , X_test, columns , scaler, graphs = False)

        return train, test,  X_train_scaled, X_test_scaled, y_train, y_test
       