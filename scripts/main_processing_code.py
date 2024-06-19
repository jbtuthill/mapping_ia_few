import os
import warnings 
warnings.filterwarnings('ignore') 
import pandas as pd

# Get the current file path and directory
current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)
os.chdir(current_directory)

# Import necessary modules and functions
from parameters_usda import (
    hogs, hogs_others, beef, milk, other_cattle, onfeed_sold, steers,
    corng_y, corng_pa, corng_ha, soy_y, soy_pa, soy_ha
)
from parameters_functions import (
    process_data_crop, process_data_animal, ap, cp
)
from validation_functions import (
    expand_df, refine_animal_data, interpolation
)
from caopeiyu_nrate import nrate

def data_processing():
    """
    Main data processing function to fetch, refine, and merge USDA animal and crop data and nitrogen rate data.
    
    Returns:
    - IFEWs_base (DataFrame): Merged DataFrame containing refined USDA data and nitrogen rate data.
    """
    # Fetch USDA data from Parameters
    animal_parameters = [hogs, hogs_others, beef, milk, other_cattle, onfeed_sold, steers]
    crop_parameters = [corng_y, corng_pa, corng_ha, soy_y, soy_pa, soy_ha]    

    animal_df = process_data_animal(animal_parameters)
    crop_df = process_data_crop(crop_parameters)

    animal_df.rename(columns={'county_name': "CountyName", 'year':'Year'}, inplace=True)
    crop_df.rename(columns={'county_name': "CountyName", 'year':'Year'}, inplace=True)

    crop_df.drop(crop_df[crop_df['CountyName'] == 'OTHER COUNTIES'].index, inplace=True)
    crop_df.drop(crop_df[crop_df['CountyName'] == 'OTHER (COMBINED) COUNTIES'].index, inplace=True)

    # Fetch validation data
    crop_val = cp()
    animal_val = ap()

    # Expand and refine USDA data
    animal_df = expand_df(df=animal_df, validation_df=crop_val)
    crop_df = expand_df(df=crop_df, validation_df=crop_val)

    # columns to numeric
    for col in [col for col in animal_df.columns if col not in ['CountyName', 'Year']]:
        animal_df[col] = pd.to_numeric(animal_df[col])

    for col in [col for col in crop_df.columns if col not in ['CountyName', 'Year']]:
        crop_df[col] = pd.to_numeric(crop_df[col])

    # Refine animal and crop data
    animal_ifews = refine_animal_data(animal_df, animal_val)
    crops_ifews = interpolation(crop_df)

    # Merge USDA data
    df_USDA = pd.merge(animal_ifews, crops_ifews, on=['CountyName', 'Year'], how='left')

    # Fetch and process nitrogen rate data
    nrate_gdf = nrate(current_directory)

    # Merge USDA data with nitrogen rate data
    IFEWs_base = pd.merge(df_USDA, nrate_gdf, on=['CountyName', 'Year'], how='inner')

    return IFEWs_base