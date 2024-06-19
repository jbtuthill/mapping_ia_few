import os
import warnings 
warnings.filterwarnings('ignore') 
import pandas as pd
import geopandas as gpd

# Set current working directory
current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)
os.chdir(current_directory)

# Import necessary functions and data processing module
from Ns_functions import (
    calculate_manure_n, calculate_fix_n, calculate_grain_n, calculate_ns, calculate_manure_n_no_storage_loss,
)
from main_processing_code import data_processing

"""
This script calculates the nitrogen surplus (Ns) based on an agronomic annual nitrogen budget.
Ns is a key indicator of water quality in the Food-Energy-Water nexus (IFEWs).

The calculation of nitrogen surplus (Ns) is given by:
Ns = CN + MN + FN - GN

where:
CN = Commercial nitrogen input
MN = Manure nitrogen input
FN = Nitrogen fixed by soybean crops
GN = Nitrogen in harvested grain

Variables:
Nrate = Commercial fertilizer in lb N/ac
x1 = Corn grain yield in tons per hectare
x2 = Soybean yield in tons per hectare
Asoy = Soybean planted area in acres
Acorn = Corn planted area in acres
AP = Total planted area in acres (Asoy + Acorn)
AH = Total harvested area in acres
P = Livestock group population in heads
Nm = Nitrogen in animal manure in kg/animal/day
LF = Life cycle of animal in days per year

Output: 
Ns = Nitrogen surplus in kg/ha
CN = Commercial nitrogen applied in planted corn crop in kg/ha
MN = Manure nitrogen generated in kg/ha (considering storage loss)
MN_old = Manure nitrogen generated in kg/ha (not considering storage loss)
FN = Nitrogen fixed by soybean crop in kg/ha
GN = Nitrogen in harvested grain in kg/ha
"""

# Process the data
IFEWs = data_processing()

# Calculate CN (Commercial Nitrogen) in kg/ha
IFEWs['CN'] = round(IFEWs["CN_lb/ac"] * 1.121, 1)

# Calculate MN (Manure Nitrogen) considering storage loss
IFEWs['MN'] = IFEWs.apply(calculate_manure_n, axis=1)

# Calculate MN_old (Manure Nitrogen) without considering storage loss
IFEWs['MN_old'] = IFEWs.apply(calculate_manure_n_no_storage_loss, axis=1)

# Calculate FN (Fixation Nitrogen)
IFEWs['FN'] = IFEWs.apply(calculate_fix_n, axis=1)

# Calculate GN (Grain Nitrogen)
IFEWs['GN'] = IFEWs.apply(calculate_grain_n, axis=1)

# Calculate Ns (Nitrogen Surplus)
IFEWs['NS'] = IFEWs.apply(calculate_ns, axis=1)

# Save the output to a GeoJSON file
# shp_path = os.path.join(current_directory, "..", "datasets", "Iowa Counties", "Counties.shp")
# shp = gpd.read_file(shp_path)
# merged_gdf = pd.merge(IFEWs, shp[['CountyName', 'geometry']], on='CountyName', how='left')
# merged_gdf = gpd.GeoDataFrame(merged_gdf, geometry='geometry', crs=shp.crs)
# output_path = os.path.join(current_directory, "..", "datasets", "IFEWs.geojson")
# merged_gdf.to_file(output_path, driver='GeoJSON')