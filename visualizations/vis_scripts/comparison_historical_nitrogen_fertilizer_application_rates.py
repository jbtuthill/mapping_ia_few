import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd
import geopandas as gpd
import os

# Set current working directory
current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)
os.chdir(current_directory)

# Load the GeoJSON files into GeoDataFrames and add a 'Year' column
gdfs = {}
for year in range(2008, 2020):
    parent_dir = os.path.abspath(os.path.join(current_directory, '../../datasets/CornRates/GJSON'))
    file_name = os.path.join(parent_dir, fr"{year}_30m_cdls_RateCorn.geojson")
    gdf = gpd.read_file(file_name)
    gdf['Year'] = year
    gdfs[year] = gdf

# Combine the GeoDataFrames, keeping only the specified columns
combined_gdf = pd.concat([
    gdfs[year][['Year', 'CornRate', 'gridcode', 'SUM_Ag_ac', 'SUM_Corn_ac', 'geometry']]
    for year in range(2008, 2020)
])

parent_dir = os.path.abspath(os.path.join(current_directory, '../vis_png'))
fname = os.path.join(parent_dir, "fig3_comparison_historical_nitrogen_fertilizer_application_rates.png")

# Define the limits
lower_limit = 155
upper_limit = 215

accepted_limit_l = 100 
accepted_limit_u = 300

total_count = combined_gdf.shape[0]
above_400_count = combined_gdf[combined_gdf['CornRate'] > 400].shape[0]
percentage_above_400 = (above_400_count / total_count) * 100
below_155_count = combined_gdf[combined_gdf['gridcode'] < 155].shape[0]
percentage_below_155 = (below_155_count / total_count) * 100

# Data Setup
rcorn_filtered = combined_gdf[combined_gdf['CornRate'] <= 1000]
bin_edges = np.linspace(0, max(rcorn_filtered['CornRate'].max(), rcorn_filtered['gridcode'].max()), num=31)
max_freq = 20  # Assuming a maximum frequency for axis scaling

# Create the grid layout
fig = plt.figure(figsize=(10, 12))
gs = gridspec.GridSpec(2, 1, height_ratios=[1, 1])  # Two plots vertically

# Settings for increased visibility
axis_font_size = 14*1.1  # Larger font for axis labels
title_font_size = 16*1.1  # Larger font for titles

# Plot for CornRate
ax1 = plt.subplot(gs[0, 0])
ax1.hist(rcorn_filtered['CornRate'], bins=bin_edges, color='#F1BE48', edgecolor='black')
ax1.axvline(lower_limit, color='firebrick', linestyle='--', label='Recommended Lower Limit (155 kg/ha)')
ax1.axvline(upper_limit, color='green', linestyle='--', label='Recommended Upper Limit (215 kg/ha)')
ax1.axvline(accepted_limit_l, color='lightcoral', linestyle='--', label='Accepted Lower Limit (100 kg/ha)')
ax1.axvline(accepted_limit_u, color='palegreen', linestyle='--', label='Accepted Upper Limit (300 kg/ha)')
ax1.set_title('Distribution of Adjusted Corn Fertilizer Rates (2008-2019):\nAlignment with Recommended Application Rates', fontsize=title_font_size)
ax1.set_xlabel('Corn Rate [kg/ha]', fontsize=axis_font_size)
ax1.set_ylabel('Frequency', fontsize=axis_font_size)
ax1.text(x=0.4, y=0.3, s=f'Rates > 400 kg/ha:\n{percentage_above_400:.2f}%', transform=ax1.transAxes, fontsize=axis_font_size)
ax1.set_ylim(0, 42000)
ax1.tick_params(axis='both', labelsize=axis_font_size*0.8)
ax1.legend(frameon= False, fontsize = axis_font_size*0.8)

# Plot for gridcode
ax2 = plt.subplot(gs[1, 0])
ax2.hist(rcorn_filtered['gridcode'], bins=bin_edges, color='#F1BE48', edgecolor='black')
ax2.axvline(lower_limit, color='firebrick', linestyle='--', label='Recommended Lower Limit (155 kg/ha)')
ax2.axvline(upper_limit, color='green', linestyle='--', label='Recommended Upper Limit (215 kg/ha)')
ax2.axvline(accepted_limit_l, color='lightcoral', linestyle='--', label='Accepted Lower Limit (100 kg/ha)')
ax2.axvline(accepted_limit_u, color='palegreen', linestyle='--', label='Accepted Upper Limit (300 kg/ha)')
ax2.set_title('Historical Nitrogen Fertilizer Use in Iowa Agricultural Ecosystems (2008-2019):\nData from Cao et al.', fontsize=title_font_size)
ax2.set_xlabel('Fertilizer Rate [kg/ha]', fontsize=axis_font_size)
ax2.set_ylabel('Frequency', fontsize=axis_font_size)
ax2.text(x=0.4, y=0.3, s=f'Rates < 155 kg/ha:\n{percentage_below_155:.2f}%', transform=ax2.transAxes, fontsize=axis_font_size)
ax2.set_ylim(0, 42000)
ax2.tick_params(axis='both', labelsize=axis_font_size*0.8)
ax2.legend(frameon= False, fontsize = axis_font_size*0.8)

# Add subplot labels
fig.text(0.01, 0.99, 'a', ha='center', va='center', fontsize=20, fontname='Times New Roman', verticalalignment='top', horizontalalignment='left', fontweight='bold')
fig.text(0.01, 0.50, 'b', ha='center', va='center', fontsize=20, fontname='Times New Roman', verticalalignment='top', horizontalalignment='left', fontweight='bold')

plt.tight_layout()
plt.savefig(fname, dpi='figure', format='png')
plt.show()