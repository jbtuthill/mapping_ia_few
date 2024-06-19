import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

def expand_df(df, validation_df):
    """
    Expand the given DataFrame to include all combinations of counties and years, filling missing values with NaN.
    
    Parameters:
    - df (DataFrame): Original DataFrame to expand.
    - validation_df (DataFrame): Validation DataFrame to determine the range of years.
    
    Returns:
    - new_df (DataFrame): Expanded DataFrame with all county-year combinations.
    """
    # Create a list of unique counties
    counties = df['CountyName'].unique()

    # Create a list of years from the minimum to the maximum year in the validation DataFrame
    years = list(range(validation_df['Year'].min(), validation_df['Year'].max() + 1))

    # Create an empty DataFrame to store the expanded data
    expanded_df = pd.DataFrame(columns=df.columns)

    # Iterate through each county and year, and add rows to the expanded DataFrame
    for county in counties:
        for year in years:
            # Check if the county and year combination already exists in the original DataFrame
            if not ((df['CountyName'] == county) & (df['Year'] == year)).any():
                # Create a new row with NaN values for all columns
                new_row = pd.DataFrame([[county, year] + [pd.NA] * (len(df.columns) - 2)], columns=df.columns)
                # Append the new row to the expanded DataFrame
                expanded_df = pd.concat([expanded_df, new_row], ignore_index=True)

    # Concatenate the original DataFrame and the expanded DataFrame
    new_df = pd.concat([df, expanded_df], ignore_index=True)

    # Sort the DataFrame by CountyName and Year
    new_df = new_df.sort_values(['CountyName', 'Year']).reset_index(drop=True)

    # Fill any remaining NaN values with appropriate default values
    new_df = new_df.fillna({'hogs': np.nan, 'hogs_sales': np.nan, 'hogs_breeding': np.nan, 'beef': np.nan, 'milk': np.nan,
                            'cattle': np.nan, 'steers': np.nan, 'onfeed_sold': np.nan, 'corng_y': np.nan, 'corng_pa': np.nan, 
                            'corng_ha': np.nan, 'soy_y': np.nan, 'soy_pa': np.nan, 'soy_ha': np.nan})
    
    # Drop duplicate rows if 'corng_y' is in the columns
    if 'corng_y' in new_df.columns:
        new_df = new_df.drop_duplicates(subset=['CountyName', 'Year'])

    # Filter out rows where Year is 2023 or later
    new_df = new_df[new_df['Year'] < 2023]

    return new_df      

def refine_animal_data(animal_df, animal_val):
    """
    Refine animal population data by interpolating missing values and proportionally distributing known values.

    Parameters:
    - animal_df (DataFrame): DataFrame containing animal population data.
    - animal_val (DataFrame): DataFrame containing validation data for animal populations.

    Returns:
    - animal_nloss (DataFrame): Refined animal population DataFrame.
    """
    animal_nloss = animal_df.copy()
    animal_val_nloss = animal_val.copy()

    # Function to distribute population among all counties proportionally
    def distribute_population_proportionally(remaining_population, counties_population):
        if not counties_population:  # Check if counties_population is empty
            return []
        
        total_known_population = sum(counties_population)
        if total_known_population == 0:
            equal_distribution = remaining_population / len(counties_population)
            return [round(equal_distribution)] * len(counties_population)
        else:
            proportions = [pop / total_known_population for pop in counties_population]
            distributed_population = [remaining_population * proportion for proportion in proportions]
            return [round(pop) for pop in distributed_population]
    
    # Function to correct values in animal population data
    def correct_values(animal_type, df, val_df, interpolated_indices):
        for year in df['Year'].unique():
            interpolated_population = df.loc[(df['Year'] == year) & df.index.isin(interpolated_indices), animal_type].tolist()
            total_interpolated_population = sum(interpolated_population)
            state_population = val_df.loc[val_df['Year'] == year, animal_type].values[0]
            total_known_population = df.loc[df['Year'] == year, animal_type].sum()

            if not np.isnan(state_population):
                remaining_population = max(0, state_population - (total_known_population - total_interpolated_population))
                corrected_population = distribute_population_proportionally(remaining_population, interpolated_population)
                df.loc[(df['Year'] == year) & df.index.isin(interpolated_indices), animal_type] = corrected_population
    
    # Function to apply linear interpolation to specific columns
    def apply_interpolation(df, columns):
        interpolated_indices = {}
        for column in columns:
            # Record indices of NaN values before interpolation
            interpolated_indices[column] = df[df[column].isna()].index.tolist()
            
            df[column] = df.groupby('CountyName')[column].transform(lambda x: x.interpolate().round())
            df[column].fillna(method='ffill', inplace=True)
            df[column].fillna(method='bfill', inplace=True)
        return interpolated_indices

    common_animal_types = set(animal_nloss.columns) & set(animal_val_nloss.columns) - {'Year', 'CountyName'}

    # Apply linear interpolation first
    interpolated_indices = apply_interpolation(animal_nloss, common_animal_types)

    # Correct only interpolated values with proportional allocation
    for animal_type in common_animal_types:
        correct_values(animal_type, animal_nloss, animal_val_nloss, interpolated_indices[animal_type])

    # Additional calculations for animal populations
    animal_nloss['bulls'] = round(animal_nloss['beef'] * 0.05)
    animal_nloss['calves'] = round(animal_nloss['cattle'] - (animal_nloss['beef'] + animal_nloss['milk'] + animal_nloss['bulls'] + animal_nloss['steers']))
    animal_nloss['beef_heifers'] = round(animal_nloss['calves'] * animal_nloss['beef'] / (animal_nloss['beef'] + animal_nloss['milk']))
    animal_nloss['dairy_150'] = round((1 / 2) * animal_nloss['calves'] * animal_nloss['milk'] / (animal_nloss['beef'] + animal_nloss['milk']))
    animal_nloss['dairy_400'] = round((1 / 2) * animal_nloss['calves'] * animal_nloss['milk'] / (animal_nloss['beef'] + animal_nloss['milk']))
    animal_nloss['fin_cattle'] = round((animal_nloss['steers'] + animal_nloss['onfeed_sold']) / 3)
    
    # Additional calculations for hog populations
    animal_nloss['hogs_fin'] = round((animal_nloss['hogs'] + animal_nloss['hogs_sales']) / 3)
    animal_nloss['hogs_sow'] = round(animal_nloss['hogs_breeding'] / 21)
    animal_nloss['hogs_boars'] = round(animal_nloss['hogs_breeding'] - animal_nloss['hogs_sow'])

    return animal_nloss

def interpolation(ifews_df):
    """
    Interpolate missing data in the given DataFrame using linear interpolation.

    Parameters:
    - ifews_df (DataFrame): DataFrame containing data to be interpolated.

    Returns:
    - df (DataFrame): DataFrame with interpolated data.
    """
    df = ifews_df.copy()
    county_names = df['CountyName'].unique()
    pop_names = ["corng_y", "corng_pa", "corng_ha", "soy_y", "soy_pa", "soy_ha"]
        
    # Loop through county names and populate data
    for county_name in county_names:
        for name in pop_names:
            k = pop_names.copy()
            k.remove(name)

            # Filter the DataFrame for the specific county and population
            county_df = df[(df['CountyName'] == county_name) & (df[name].notna())]

            # Extract x and y values
            x = county_df['Year'].astype(float).to_numpy()
            y = county_df[name].astype(float).to_numpy()

            # Extract xnew values
            xnew = df[(df['CountyName'] == county_name) & (df[name].isna())]['Year'].astype(float).to_numpy()

            f = interp1d(x, y, kind='linear', fill_value="extrapolate")
            ynew = f(xnew)

            # Update the DataFrame with interpolated values
            df.loc[(df['CountyName'] == county_name) & (df[name].isna()), name] = np.round(ynew)

    # Replace negative values with zero in the entire DataFrame
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].apply(lambda x: 0 if x < 0 else x)

    # Forward fill consecutive zeros with the last previous value
    df = df.apply(lambda x: x.mask(x == 0).ffill())
    
    return df