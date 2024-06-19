# IFEWs Data Processing Scripts
This folder contains the scripts used for data processing and analysis in the study "Mapping the Nexus: A County-Level Analysis and Visualization of Iowa's Food-Energy-Water Systems." The scripts are designed to handle various aspects of the project, including fetching and processing USDA data, calculating nitrogen surplus, and integrating multiple data sources.

## Scripts Overview
### 1. caopeiyu_nrate.py
This script processes original nitrogen fertilizer data from rasters to points and aggregates them to counties. It reads boundary data and processes raster files to generate GeoJSON files containing nitrogen rate data for each year.

### 2. main_processing_code.py
This is the script that orchestrates the data processing workflow. It fetches USDA data, processes animal and crop data, validates and refines the data, and integrates nitrogen rate data from the caopeiyu_nrate.py script.

### 3. main_Ns_code.py
This script calculates the nitrogen surplus (Ns) based on the processed data. It uses the data processed by main_code.py and applies various functions to calculate the components of nitrogen surplus, including commercial nitrogen, manure nitrogen, fixation nitrogen, and grain nitrogen.

### 4. Ns_functions.py
This script contains functions for calculating different components of nitrogen surplus:

- calculate_manure_n: Calculates manure nitrogen considering storage loss.
- calculate_fix_n: Calculates fixation nitrogen.
- calculate_grain_n: Calculates grain nitrogen.
- calculate_ns: Calculates nitrogen surplus.
- calculate_manure_n_no_storage_loss: Calculates manure nitrogen without considering storage loss.

### 5. parameters_functions.py
This script defines functions to fetch and process animal and crop data for the State of Iowa:

- ap: Fetches and processes animal population data.
- cp: Fetches and processes crop production data.
- process_data_crop: Processes crop data based on provided parameters.
- process_data_animal: Processes animal data based on provided parameters.

### 6. parameters_usda.py
This script contains the parameters used to fetch specific USDA data. It defines the query parameters for various crop and animal statistics from the USDA QuickStats API.

### 7. USDAQuickStats.py
This script defines a class to interact with the USDA QuickStats API. It includes methods to encode parameters and fetch data from the API.

### 8. validation_functions.py
This script contains functions for validating and refining the processed data:

- expand_df: Expands the DataFrame to include all combinations of counties and years.
- refine_animal_data: Refines animal data by correcting values and applying linear interpolation.
- interpolation: Applies linear interpolation to fill missing data points.

### 9. MinimizeSSE.xlsx
Excel file used for minimizing the sum of squared errors (SSE) in the analysis. It uses the Solver add-in in Excel to optimize the parameters.

This Excel file includes data and formulas used for minimizing the sum of squared errors in the analysis. It is used to fit models that predict ethanol production based on corn usage. The file is set up to use the Solver add-in in Excel with the following settings:

- Objective: Minimize the sum value of the error squared between EIA reported Thousand Barrel and IFEWs method Thousand barrels in the years of 2005 till 2019 in cell $L$36.
- Variable Cells: Change cell $N$2.
- Constraints: IFEWs value should not be greater than EIA reported values.
- Solving Method: GRG Nonlinear

## Usage
Setting Up the Environment:

Ensure you have all the necessary dependencies installed.
Place the env file containing your API key in the appropriate directory.
Running the Scripts:

Start by running main_Ns_code.py to process the USDA data and integrate nitrogen rate data using  data_processing function from main_processing_code.py. Then, the output will be yearly county nitrogen surplus from 1968 till 2019. 
Output:

The final integrated data can be saved as a GeoJSON file in a specified output directory. The file is currently available in ../datasets/IFEWs.geojson

## Dependencies
- Python 3.x
- pandas
- geopandas
- rioxarray
- rasterio
- rasterstats
- numpy
- urllib
- shapely