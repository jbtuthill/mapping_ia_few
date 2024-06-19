import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.lines as mlines
import numpy as np
from matplotlib.ticker import FuncFormatter
import pandas as pd
import geopandas as gpd
from sklearn.metrics import r2_score
import warnings 
warnings.filterwarnings('ignore') 
import os

# Set current working directory
current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)
os.chdir(current_directory)

functions_dir = os.path.abspath(os.path.join(current_directory, '../../scripts'))
os.chdir(functions_dir)
from parameters_usda import (
    hogs, hogs_others, beef, milk, other_cattle, onfeed_sold, steers,
)
from parameters_functions import (
    process_data_animal, ap, cp
)
from validation_functions import (
    expand_df, refine_animal_data
)

ifews = gpd.read_file(os.path.join(os.path.abspath(os.path.join(current_directory, '../../datasets/')), "IFEWs.geojson"))
ifews['Year'] = pd.to_numeric(ifews['Year'])
parent_dir = os.path.abspath(os.path.join(current_directory, '../vis_png'))

animal_parameters = [hogs, hogs_others, beef, milk, other_cattle, onfeed_sold, steers]
# Process animal and crop data
animal_df = process_data_animal(animal_parameters)

animal_df.rename(columns={'county_name': "CountyName", 'year':'Year'
            }, inplace=True)

# ---------------------Validation - Yearly values for Iowa from USDA ----------------------
crop_val = cp()
animal_val = ap()

animal_df = expand_df(df = animal_df, validation_df = crop_val)

cols = [ i for i in animal_df.columns if i not in ['CountyName', 'Year']]
for col in cols:
    animal_df[col] = pd.to_numeric(animal_df[col])

animal_ifews = refine_animal_data(animal_df, animal_val)    

def USDA_IFEWs_plot(IFEWs, parent_dir, animal_df):
    # Create the grid layout
    fig = plt.figure(figsize=(10, 12))
    gs = gridspec.GridSpec(2, 1, height_ratios=[1, 1])  # Adjusted to have only two plots vertically

    # Settings for increased visibility
    marker_size = 13*2*2  # Larger marker size
    legend_font_size = 14*1.1  # Larger font for the legend
    axis_font_size = 14*1.1  # Larger font for axis labels
    title_font_size = 16*1.1  # Larger font for titles

    # Define custom lines for the legend (assuming they are defined somewhere above)
    lines = [
        mlines.Line2D([], [], color='#C8102E', marker='o', linestyle='', markersize=6, label='Hogs pre-interpolation'),
        mlines.Line2D([], [], color='#fac2cb', linestyle='-', label='Hogs after interpolation'),
        mlines.Line2D([], [], color='#f1be48', marker='o', linestyle='', markersize=6, label='Beef Cattle pre-interpolation'),
        mlines.Line2D([], [], color='#ffecaf', linestyle='-', label='Beef Cattle after interpolation'),
        mlines.Line2D([], [], color='#706e67', marker='o', linestyle='', markersize=6, label='Cattle on Feed Sold pre-interpolation'),
        mlines.Line2D([], [], color='#dad6d4', linestyle='-', label='Cattle on Feed Sold after interpolation')
    ]

    # Adair County Plot on position 1 of grid (top)
    ax1 = plt.subplot(gs[0, 0])

    # Plot settings for Adair County
    ax1.plot(IFEWs[IFEWs['CountyName'] == 'ADAIR']['Year'], IFEWs[IFEWs['CountyName'] == 'ADAIR']['hogs']/1e6, linestyle='-', color='#fac2cb', zorder=0)
    ax1.scatter(animal_df[animal_df['CountyName'] == 'ADAIR']['Year'], animal_df[animal_df['CountyName'] == 'ADAIR']['hogs']/1e6, color='#C8102E', s=marker_size, zorder=1)

    ax1.plot(IFEWs[IFEWs['CountyName'] == 'ADAIR']['Year'], IFEWs[IFEWs['CountyName'] == 'ADAIR']['beef']/1e6, linestyle='-', color='#ffecaf', zorder=0)
    ax1.scatter(animal_df[animal_df['CountyName'] == 'ADAIR']['Year'], animal_df[animal_df['CountyName'] == 'ADAIR']['beef']/1e6, color='#f1be48', s=marker_size, zorder=1)

    ax1.plot(IFEWs[IFEWs['CountyName'] == 'ADAIR']['Year'], IFEWs[IFEWs['CountyName'] == 'ADAIR']['onfeed_sold']/1e6, linestyle='-', color='#dad6d4', zorder=0)
    ax1.scatter(animal_df[animal_df['CountyName'] == 'ADAIR']['Year'], animal_df[animal_df['CountyName'] == 'ADAIR']['onfeed_sold']/1e6, color='#706e67', s=marker_size, zorder=1)

    # Set axis and legend properties
    ax1.set_xlim(1967, 2021)
    ax1.set_ylabel('Population [millions]', fontsize=axis_font_size)
    ax1.set_xlabel('Year', fontsize=axis_font_size)
    ax1.tick_params(axis='both', labelsize=axis_font_size)
    ax1.set_title('Adair County', fontsize=title_font_size)
    ax1.legend(handles=lines, loc='upper right', fontsize=legend_font_size, frameon=False, scatterpoints=1, markerscale=1)  # Adjust legend marker size

    # Sioux County Plot on position 2 of grid (bottom)
    ax2 = plt.subplot(gs[1, 0])

    # Plot settings for Sioux County
    ax2.plot(IFEWs[IFEWs['CountyName'] == 'SIOUX']['Year'], IFEWs[IFEWs['CountyName'] == 'SIOUX']['hogs']/1e6, linestyle='-', color='#fac2cb', zorder=0)
    ax2.scatter(animal_df[animal_df['CountyName'] == 'SIOUX']['Year'], animal_df[animal_df['CountyName'] == 'SIOUX']['hogs']/1e6, color='#C8102E', s=marker_size, zorder=1)

    ax2.plot(IFEWs[IFEWs['CountyName'] == 'SIOUX']['Year'], IFEWs[IFEWs['CountyName'] == 'SIOUX']['beef']/1e6, linestyle='-', color='#ffecaf', zorder=0)
    ax2.scatter(animal_df[(animal_df['CountyName'] == 'SIOUX') & (animal_df['Year'] <= 2019)]['Year'], animal_df[(animal_df['CountyName'] == 'SIOUX') & (animal_df['Year'] <= 2019)]['beef']/1e6, color='#f1be48', s=marker_size, zorder=1)

    ax2.plot(IFEWs[IFEWs['CountyName'] == 'SIOUX']['Year'], IFEWs[IFEWs['CountyName'] == 'SIOUX']['onfeed_sold']/1e6, linestyle='-', color='#dad6d4', zorder=0)
    ax2.scatter(animal_df[animal_df['CountyName'] == 'SIOUX']['Year'], animal_df[animal_df['CountyName'] == 'SIOUX']['onfeed_sold']/1e6, color='#706e67', s=marker_size, zorder=1)

    # Set axis and legend properties
    ax2.set_xlim(1967, 2021)
    ax2.set_ylabel('Population [millions]', fontsize=axis_font_size)
    ax2.set_xlabel('Year', fontsize=axis_font_size)
    ax2.tick_params(axis='both', labelsize=axis_font_size)
    ax2.set_title('Sioux County', fontsize=title_font_size)

    fig.text(0.010, 0.99, 'a', ha='center', va='center', fontsize=20, fontname='Times New Roman', verticalalignment='top', horizontalalignment='left', fontweight='bold')
    fig.text(0.01, 0.50, 'b', ha='center', va='center', fontsize=20, fontname='Times New Roman', verticalalignment='top', horizontalalignment='left', fontweight='bold')

    fname = os.path.join(parent_dir, "fig6_animal_pop_sioux_vs_adair.png")

    plt.tight_layout()
    plt.savefig(fname, dpi='figure', format='png')
    plt.show()

USDA_IFEWs_plot(ifews, parent_dir, animal_df)


def plot_hogs_comparison(animal_df, df, val):
    # Initialize a dictionary to store R^2 values for each animal type
    r_squared_results = {}

    # List of all animal types to calculate R^2 values for
    animal_types = ['beef', 'milk', 'cattle', 'steers', 'onfeed_sold', 'hogs', 'hogs_breeding', 'hogs_sales']

    def rsq(ifews, validation, animal_type):
        for animal in animal_type:
            df_year = ifews.groupby('Year')[animal].sum() 
            df = df_year[df_year.index <= 2019] 

            val = validation[validation['Year'] <= 2019]
            val = val[['Year', animal]]
            val.set_index('Year', inplace=True)

                    # Reindex the predictions to match the validation set's index and drop NaNs
            y_pred = df.reindex(val.index).dropna()
            y_true = val[animal].dropna()
            
            # Ensure both Series have the same index for valid comparison
            common_indices = y_true.index.intersection(y_pred.index)
            y_true = y_true.loc[common_indices]
            y_pred = y_pred.loc[common_indices]

            # Calculate R2 score, handle cases where there are NaN values or insufficient data
            if not y_true.empty and not y_pred.empty:
                #r_squared = r2_score(y_true, y_pred)
                r_squared = round(r2_score(y_true, y_pred),5)            
                r_squared_results[animal] = r_squared
            else:
                print(f'Error for {animal}')


    rsq(animal_ifews, animal_val, animal_types)
    r_squared_results

    marker_size = 8  # Larger marker size
    legend_font_size = 14*1.1  # Larger font for the legend
    axis_font_size = 14*1.1  # Larger font for axis labels
    title_font_size = 16*1.1  # Larger font for titles

    fig, ax = plt.subplots(figsize=(10, 6))

    animal_df = animal_df[animal_df['Year'] <= 2019]
    df = df[df['Year'] <= 2019]
    # Plotting non-interpolated values
    non_interpolated_values = animal_df.groupby('Year')['hogs'].sum() / 1_000_000  # Scale to millions
    # Filter out zero and NaN values, marking NaNs as 'Suppressed'
    non_interpolated_values = non_interpolated_values.replace(0, np.nan)
    valid_indices = ~non_interpolated_values.isnull()

    # Plot only the non-zero and non-NaN values
    ax.plot(non_interpolated_values[valid_indices].index, non_interpolated_values[valid_indices], 
            marker='o', linestyle='', color='#C8102E', alpha=0.5, label='Non-Interpolated', zorder=2, markersize= marker_size, markeredgewidth=0.0)

    # Plotting interpolated values
    interpolated_values = df.groupby('Year')['hogs'].sum() / 1_000_000  # Scale to millions
    ax.plot(interpolated_values.index, interpolated_values,  linestyle='-', color='#F1BE48', label='Interpolated', zorder=0)
    
    val = val[val['Year'] <= 2019]
    # Plotting validation values
    val_hogs_millions = val['hogs'] / 1_000_000  # Scale to millions
    ax.plot(val['Year'], val_hogs_millions, linestyle='dotted', color='#524727', label='Validation (State-level)', zorder=1)

    # Adding labels and title
    ax.set_xlabel('Year', fontsize=axis_font_size)
    ax.set_ylabel('Population (Millions)', fontsize=axis_font_size)
    ax.set_title('Hogs Population Over the Years', fontsize=title_font_size)

    # Set y-axis to display actual numbers instead of scientific notation
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, _: format(int(x), ',')))

    ax.tick_params(axis='both', labelsize=12)
    ax.set_xlim(1967, 2021)
    ax.set_ylim(11.5, 25)  # Adjusted for millions

    # Add the legend
    ax.legend(fontsize=legend_font_size, frameon=False)
        
    r_squared = r_squared_results['hogs']
    plt.text(0.7, 0.89, f'$R^2 = {r_squared:.5f}$', ha='left', va='top', fontsize=20, fontname='Times New Roman', fontweight='bold', transform=plt.gca().transAxes)

    fname = os.path.join(parent_dir, "fig7_state_level_usda_vs_ifews.png")

    plt.tight_layout()
    plt.savefig(fname, dpi='figure', format='png')
    plt.show()

plot_hogs_comparison(animal_df, animal_ifews, animal_val)