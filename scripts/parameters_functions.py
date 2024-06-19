import os
import pandas as pd
import numpy as np
import urllib.parse
current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)
os.chdir(current_directory)
from USDAQuickStats import USDAQuickStats

# Initialize USDAQuickStats class with your API key
stats = USDAQuickStats(os.getenv('API_KEY'))

def ap():
    """
    Fetch and process animal population data for the State of Iowa.
    
    Returns:
    - merged_data (DataFrame): A pandas DataFrame containing processed animal population data.
    """
    # Fetch cattle data
    ap_cbval = pd.read_csv('https://api.usda-reports.penguinlabs.net/data.csv?short_desc=CATTLE%2C+COWS%2C+BEEF+-+INVENTORY&year__GE=1968&agg_level_desc=STATE&reference_period_desc=FIRST+OF+JAN')
    ap_cbval = ap_cbval[ap_cbval['state_name'] == 'IOWA'][['Value', 'year']]
    ap_cbval.rename(columns={'Value': 'beef'}, inplace=True)
    
    ap_cmval = pd.read_csv('https://api.usda-reports.penguinlabs.net/data.csv?short_desc=CATTLE%2C+COWS%2C+MILK+-+INVENTORY&year__GE=1968&agg_level_desc=STATE&reference_period_desc=FIRST+OF+JAN')
    ap_cmval = ap_cmval[ap_cmval['state_name'] == 'IOWA'][['Value', 'year']]
    ap_cmval.rename(columns={'Value': 'milk'}, inplace=True)
    
    ap_cicval = pd.read_csv('https://api.usda-reports.penguinlabs.net/data.csv?short_desc=CATTLE%2C+INCL+CALVES+-+INVENTORY&year__GE=1968&agg_level_desc=STATE&reference_period_desc=FIRST+OF+JAN')
    ap_cicval = ap_cicval[ap_cicval['state_name'] == 'IOWA'][['Value', 'year']]
    ap_cicval.rename(columns={'Value': 'cattle'}, inplace=True)

    # Fetch on feed data
    on_feed_s = (
        urllib.parse.quote('sector_desc=ANIMALS & PRODUCTS') + \
                '&group_desc=LIVESTOCK' + \
                '&commodity_desc=CATTLE' + \
                '&' + urllib.parse.quote('prodn_practice_desc=ON FEED') + \
                '&' + urllib.parse.quote('domain_desc=SALES') + \
                '&unit_desc=HEAD' + \
                '&year__GE=1968' + \
                '&agg_level_desc=STATE' + \
                '&state_name=IOWA' + \
                '&format=CSV'
    )
    
    df = stats.get_data(on_feed_s)

    # Process cattle steers data
    ap_csval = df[(df['short_desc'] == 'CATTLE, ON FEED - INVENTORY') & (df['domain_desc'] == 'TOTAL')][['Value', 'year']]
    ap_csval.rename(columns={'Value': 'steers'}, inplace=True)

    # Process cattle for sale data
    ap_sval = df[(df['short_desc'] == 'CATTLE, ON FEED - SALES FOR SLAUGHTER, MEASURED IN HEAD') & (df['domain_desc'] == 'TOTAL')][['Value', 'year']]
    ap_sval.rename(columns={'Value': 'onfeed_sold'}, inplace=True)
    
    # Fetch hogs data
    ap_hval = pd.read_csv('https://api.usda-reports.penguinlabs.net/data.csv?short_desc=HOGS+-+INVENTORY&year__GE=1968&agg_level_desc=STATE&reference_period_desc=FIRST+OF+DEC')
    ap_hval = ap_hval[ap_hval['state_name'] == 'IOWA'][['Value', 'year']]
    ap_hval.rename(columns={'Value': 'hogs'}, inplace=True)
    
    ap_hbval = pd.read_csv('https://api.usda-reports.penguinlabs.net/data.csv?short_desc=HOGS,+BREEDING+-+INVENTORY&year__GE=1968&agg_level_desc=STATE&reference_period_desc=FIRST+OF+DEC')
    ap_hbval = ap_hbval[ap_hbval['state_name'] == 'IOWA'][['Value', 'year']]
    ap_hbval.rename(columns={'Value': 'hogs_breeding'}, inplace=True)
    
    ap_hsval = pd.read_csv('https://api.usda-reports.penguinlabs.net/data.csv?short_desc=HOGS+-+SALES,+MEASURED+IN+HEAD&year__GE=1968&agg_level_desc=STATE&reference_period_desc=YEAR')
    ap_hsval = ap_hsval[ap_hsval['state_name'] == 'IOWA'][['Value', 'year']]
    ap_hsval.rename(columns={'Value': 'hogs_sales'}, inplace=True)

    # Merge all data
    merged_data = ap_cbval.merge(ap_cmval, on='year', how='outer')\
                          .merge(ap_cicval, on='year', how='outer')\
                          .merge(ap_csval, on='year', how='outer')\
                          .merge(ap_sval, on='year', how='outer')\
                          .merge(ap_hval, on='year', how='outer')\
                          .merge(ap_hbval, on='year', how='outer')\
                          .merge(ap_hsval, on='year', how='outer')

    merged_data = merged_data.replace(',', '', regex=True)
    cols = merged_data.columns.drop('year')
    merged_data[cols] = merged_data[cols].apply(pd.to_numeric, errors='coerce')
    merged_data.rename(columns={'year': 'Year'}, inplace=True)

    return merged_data  

def cp():
    """
    Fetch and process crop production data for the State of Iowa.
    
    Returns:
    - merged_data (DataFrame): A pandas DataFrame containing processed crop production data.
    """
    # Fetch crop production data
    cp_cyval = pd.read_csv('https://api.usda-reports.penguinlabs.net/data.csv?short_desc=CORN%2C+GRAIN+-+YIELD%2C+MEASURED+IN+BU+%2F+ACRE&year__GE=1968&agg_level_desc=STATE')
    cp_cyval = cp_cyval[cp_cyval['state_name'] == 'IOWA'][['Value', 'year']]
    cp_cyval.rename(columns={'Value': 'corng_y'}, inplace=True)
    
    cp_chval = pd.read_csv('https://api.usda-reports.penguinlabs.net/data.csv?short_desc=CORN%2C+GRAIN+-+ACRES+HARVESTED&year__GE=1968&agg_level_desc=STATE')
    cp_chval = cp_chval[cp_chval['state_name'] == 'IOWA'][['Value', 'year']]
    cp_chval.rename(columns={'Value': 'corng_ha'}, inplace=True)
    
    cp_cpval = pd.read_csv('https://api.usda-reports.penguinlabs.net/data.csv?short_desc=CORN+-+ACRES+PLANTED&year__GE=1968&agg_level_desc=STATE')
    cp_cpval = cp_cpval[cp_cpval['state_name'] == 'IOWA'][['Value', 'year']]
    cp_cpval.rename(columns={'Value': 'corng_pa'}, inplace=True)
    
    cp_syval = pd.read_csv('https://api.usda-reports.penguinlabs.net/data.csv?short_desc=SOYBEANS+-+YIELD%2C+MEASURED+IN+BU+%2F+ACRE&year__GE=1968&agg_level_desc=STATE')
    cp_syval = cp_syval[cp_syval['state_name'] == 'IOWA'][['Value', 'year']]
    cp_syval.rename(columns={'Value': 'soy_y'}, inplace=True)
    
    cp_shval = pd.read_csv('https://api.usda-reports.penguinlabs.net/data.csv?short_desc=SOYBEANS+-+ACRES+HARVESTED&year__GE=1968&agg_level_desc=STATE')
    cp_shval = cp_shval[cp_shval['state_name'] == 'IOWA'][['Value', 'year']]
    cp_shval.rename(columns={'Value': 'soy_ha'}, inplace=True)
    
    cp_spval = pd.read_csv('https://api.usda-reports.penguinlabs.net/data.csv?short_desc=SOYBEANS+-+ACRES+PLANTED&year__GE=1968&agg_level_desc=STATE')
    cp_spval = cp_spval[cp_spval['state_name'] == 'IOWA'][['Value', 'year']]
    cp_spval.rename(columns={'Value': 'soy_pa'}, inplace=True)

    # Merge all data
    merged_data = pd.merge(cp_cyval, cp_chval, on='year', how='outer')
    merged_data = pd.merge(merged_data, cp_cpval, on='year', how='outer')
    merged_data = pd.merge(merged_data, cp_syval, on='year', how='outer')
    merged_data = pd.merge(merged_data, cp_shval, on='year', how='outer')
    merged_data = pd.merge(merged_data, cp_spval, on='year', how='outer')

    merged_data = merged_data.replace(',', '', regex=True)
    cols = merged_data.columns.drop('year')
    merged_data[cols] = merged_data[cols].apply(pd.to_numeric, errors='coerce')
    merged_data.rename(columns={'year': 'Year'}, inplace=True)

    return merged_data  

def process_data_crop(parameters):
    """
    Process Iowa counties crop data based on provided parameters.

    Parameters:
    - parameters (list): List of parameters for fetching crop data.

    Returns:
    - df (DataFrame): A pandas DataFrame containing processed crop data.
    """
    dataframes = []
    for param in parameters:
        df = stats.get_data(param)         

        if 'CORN' in param and 'YIELD' in param:
            name = "corng_y"
        elif 'CORN' in param and 'PLANTED' in param:
            name = "corng_pa"  
        elif 'CORN' in param and 'HARVESTED' in param:
            name = "corng_ha"  
        elif 'SOYBEANS' in param and 'YIELD' in param:
            name = "soy_y"
        elif 'SOYBEANS' in param and 'HARVESTED' in param:
            name = "soy_ha"
        else:
            name = "soy_pa"
        
        # Pivot table with county_name and year as indices and Value as the data column
        df = df.pivot_table(index=['county_name', 'year'], 
                            values='Value', 
                            aggfunc='first').reset_index()

        # Rename the columns
        df.columns = ['county_name', 'year', name]

        dataframes.append(df)

    df = dataframes[0] 
    for dfs in dataframes[1:]:  # Loop through remaining dataframes
        df = pd.merge(df, dfs, on=['county_name', 'year'], how='outer')
    
    df = df.replace(',', '', regex=True)
    df = df.replace(' (D)', np.nan)
    
    return df

def process_data_animal(parameters):
    """
    Process Iowa counties animal data based on provided parameters.

    Parameters:
    - parameters (list): List of parameters for fetching animal data.

    Returns:
    - df (DataFrame): A pandas DataFrame containing processed animal data.
    """
    dataframes = []
    for param in parameters:
        df = stats.get_data(param)
        
        if 'CALVES' in param:
            df = df[df['class_desc'] == 'INCL CALVES']
            # Pivot table with county_name and year as indices and Value as the data column
            df = df.pivot_table(index=['county_name', 'year'], 
                                values='Value', 
                                aggfunc='first').reset_index()
            df.columns = ['county_name', 'year', 'cattle']

        if 'HOGS' in param and 'BREEDING' not in param:
            df = df[df['short_desc'] == 'HOGS - INVENTORY']  
            # Pivot table with county_name and year as indices and Value as the data column
            df = df.pivot_table(index=['county_name', 'year'], 
                                values='Value', 
                                aggfunc='first').reset_index()
            df.columns = ['county_name', 'year', 'hogs']

        if 'BREEDING' in param:  
            df = df[
                ((df['short_desc'] == 'HOGS, BREEDING - INVENTORY') | 
                (df['short_desc'] == 'HOGS - SALES, MEASURED IN HEAD')) & 
                (df['domain_desc'] == 'TOTAL')
            ][['county_name', 'year', 'short_desc', 'Value']]
            # Use pivot_table to reshape the data
            df = df.pivot_table(
                index=['county_name', 'year'], 
                columns='short_desc', 
                values='Value', 
                aggfunc='first'
            ).reset_index()
            df.columns.name = None  # Remove the columns' name
            df.rename(columns={
                'HOGS, BREEDING - INVENTORY': 'hogs_breeding', 
                'HOGS - SALES, MEASURED IN HEAD': 'hogs_sales'
            }, inplace=True)
            
        if 'SALES' in param:
            df = df[
                ((df['short_desc'] == 'CATTLE, ON FEED - INVENTORY') | 
                (df['short_desc'] == 'CATTLE, ON FEED - SALES FOR SLAUGHTER, MEASURED IN HEAD')) & 
                (df['domain_desc'] == 'TOTAL')
            ][['county_name', 'year', 'short_desc', 'Value']]
            df = df.pivot_table(
                index=['county_name', 'year'], 
                columns='short_desc', 
                values='Value', 
                aggfunc='first'
            ).reset_index()
            df.columns.name = None
            df.rename(columns={
                'CATTLE, ON FEED - INVENTORY': 'steers', 
                'CATTLE, ON FEED - SALES FOR SLAUGHTER, MEASURED IN HEAD': 'onfeed_sold'
            }, inplace=True)
            
        if not any(x in param for x in ['CHICKENS', 'SALES', 'BREEDING', 'HOGS', 'CALVES']):
            if 'BEEF' in param:
                name = "beef"
            elif 'MILK' in param:
                name = "milk"

            # Pivot table with county_name and year as indices and Value as the data column
            df = df.pivot_table(index=['county_name', 'year'], 
                                values='Value', 
                                aggfunc='first').reset_index()
            df.columns = ['county_name', 'year', name]

        dataframes.append(df)

    df = dataframes[0] 
    for dfs in dataframes[1:]: 
        df = pd.merge(df, dfs, on=['county_name', 'year'], how='outer')
        
    if 'milk_y' in df.columns:
        df = df.drop(columns=['milk_y'])
    if 'milk_x' in df.columns:
        df = df.rename(columns={'milk_x': 'milk'})   
    
    df = df.replace(',', '', regex=True)
    df = df.replace(' (D)', np.nan)
    
    return df