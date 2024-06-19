import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import warnings 
import numpy as np
warnings.filterwarnings('ignore') 
from matplotlib.cm import ScalarMappable
from matplotlib.colors import LinearSegmentedColormap, Normalize
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import seaborn as sns
import os

# Set current working directory
current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)
os.chdir(current_directory)

parent_dir = os.path.abspath(os.path.join(current_directory, '../vis_png'))

# IFEWs data
gdf = gpd.read_file(os.path.join(os.path.abspath(os.path.join(current_directory, '../../datasets/')), "IFEWs.geojson"))
gdf['Year_num'] = pd.to_numeric(gdf['Year'])
gdf['NS_num'] = pd.to_numeric(gdf['NS'])
gdf = gdf.to_crs("EPSG:3857")
gdf = gpd.GeoDataFrame(gdf, geometry='geometry')

# Define the years of interest
years = [1968, 1978, 1988, 1998, 2008, 2018]
vmin = gdf['NS_num'].min()
vmax = gdf['NS_num'].max()

def ns_spatial_temporal(gdf, parent_dir):
 
    colors = ['#CAC7A7', 'white', '#F1BE48', '#C8102E']

    # Adjust the positions so that white corresponds to zero
    midpoint = -vmin / (vmax - vmin)
    positions = [0, midpoint, (midpoint + 0.05), 1]
    cmap = LinearSegmentedColormap.from_list('custom_colormap', list(zip(positions, colors)))

    # Create a subplot for each year
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(15, 10))

    # Iterate over the years and plot the NS for each Iowa county
    for i, year in enumerate(years):
        ax = axes[i // 3, i % 3]
        gdf_year = gdf[gdf['Year_num'] == year]
        im = gdf_year.plot(column='NS_num', ax=ax, cmap=cmap, vmin=vmin, vmax=vmax)
        ax.set_title(f'{year}', fontsize = 20)
        ax.axis('off')

    # Create a ScalarMappable object for the colorbar
    norm = Normalize(vmin=vmin, vmax=vmax)
    sm = ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])  

    # Add a colorbar at the bottom of the figure
    cax = fig.add_axes([0.1, 0.05, 0.8, 0.02]) 
    fig.colorbar(sm, cax=cax, orientation='horizontal')
    cax.tick_params(labelsize=18)

    fname = os.path.join(parent_dir, "fig9_decadal_variations_ns.png")

    plt.tight_layout()
    plt.savefig(fname, dpi='figure', format='png')
    plt.show()

ns_spatial_temporal(gdf, parent_dir)

def ns_breakdown(gdf, parent_dir):

    selected_years = ["1968", "1978", "1988", "1998", "2008", "2018"]
    selected_counties = ['SIOUX', 'STORY', 'WASHINGTON', 'POLK', 'FREMONT', 'LEE', 'LYON', 'MADISON', 'WAYNE', 'BUENA VISTA']

    max_value = gdf[(gdf['Year'].isin(selected_years)) & (gdf['CountyName'].isin(selected_counties))][['CN', 'FN', 'MN']].sum(axis=1).max() + 20
    min_value = -gdf[(gdf['Year'].isin(selected_years)) & (gdf['CountyName'].isin(selected_counties))]['GN'].max() - 20

    legend_font_size = 18 * 1.1
    axis_font_size = 18 * 1.1
    title_font_size = 20 * 1.1

    fig = plt.figure(figsize=(24, 12))
    gs = gridspec.GridSpec(2, 4)

    for j, year in enumerate(selected_years):
        ax = fig.add_subplot(gs[j // 3, j % 3])  
        filtered_data = gdf[(gdf['Year'] == year) & (gdf['CountyName'].isin(selected_counties))]
        n_bars = len(filtered_data)
        for i, (index, row) in enumerate(filtered_data.iterrows()):
            plt.bar(i, row['CN'], label='CN' if i == 0 and j == 0 else "", color='#C8102E')
            plt.bar(i, row['FN'], bottom=row['CN'], label='FN' if i == 0 and j == 0 else "", color='#F1BE48')
            plt.bar(i, row['MN'], bottom=row['CN'] + row['FN'], label='MN' if i == 0 and j == 0 else "", color='#524727')
            plt.bar(i, -row['GN'], label='GN' if i == 0 and j == 0 else "", color='#CAC7A7')

        if j < 3:
            ax.xaxis.set_visible(False)
        else:
            plt.xticks(range(n_bars), [row['CountyName'] for index, row in filtered_data.iterrows()], rotation=90)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        if j % 3 == 0:
            plt.tick_params(axis='both', labelsize=17)
            if j == 0:
                plt.legend(frameon=False, fontsize=legend_font_size)
        else:
            plt.tick_params(axis='both', labelsize=17)
            ax.set_yticks([])
            ax.spines['left'].set_visible(False)
        plt.title(year, fontsize=title_font_size)
        ax.set_ylim(min_value, max_value)
    fig.text(-0.01, 0.5, 'Nitrogen Surplus Contribution kg/ha', va='center', rotation='vertical', fontsize=axis_font_size)

    ax_inset = fig.add_subplot(gs[:, 3])
    base = gdf.plot(ax=ax_inset, color='none', edgecolor='black', linewidth=0.3)
    colors = plt.get_cmap('tab10', len(selected_counties))

    patches = [] 
    for idx, county in enumerate(selected_counties):
        highlighted = gdf[(gdf['CountyName'] == county)]
        color = colors(idx)
        highlighted.plot(ax=base, color=color, edgecolor='black', linewidth=0.5)
        patches.append(mpatches.Patch(color=color, label=county)) 

    ax_inset.legend(handles=patches, loc='lower center', frameon=False, fontsize=14, ncol=2, bbox_to_anchor=(0.5, -0.7))

    ax_inset.set_xticks([])
    ax_inset.set_yticks([])
    ax_inset.spines['top'].set_visible(False)
    ax_inset.spines['right'].set_visible(False)
    ax_inset.spines['left'].set_visible(False)
    ax_inset.spines['bottom'].set_visible(False)

    fname = os.path.join(parent_dir, "fig10_breakdown_ns.png")

    plt.tight_layout()
    plt.savefig(fname, dpi='figure', format='png')
    plt.show()

ns_breakdown(gdf, parent_dir)

def ns_methods_trends(gdf, parent_dir):
    avg_CN__by_year = gdf.groupby(['CountyName', 'Year'])['CN'].mean().unstack()
    # Define a function to calculate the slope of a linear regression
    def calculate_slope(x, y):
        return np.polyfit(x, y, 1)[0]

    # Define the years for the two periods
    years_prior_1975 = list(range(1968, 1975))
    years_1975_1990 = list(range(1975, 1990))
    years_1990_2005 = list(range(1990, 2005))
    years_2005_2019 = list(range(2005, 2020))

    # Calculate the slope for each county for each period
    slopes_prior_1975  = avg_CN__by_year .loc[:, '1968':'1974'].apply(lambda x: calculate_slope(years_prior_1975, x), axis=1)
    slopes_1975_1990 = avg_CN__by_year .loc[:, '1975':'1989'].apply(lambda x: calculate_slope(years_1975_1990, x), axis=1)
    slopes_1990_2004 = avg_CN__by_year .loc[:, '1990':'2004'].apply(lambda x: calculate_slope(years_1990_2005, x), axis=1)
    slopes_2005_2019 = avg_CN__by_year .loc[:, '2005':'2019'].apply(lambda x: calculate_slope(years_2005_2019, x), axis=1)

    # Combine the slopes into a single DataFrame
    slopes_df = pd.DataFrame({
        'Slope_prior_1975': slopes_prior_1975,
        'Slope_1975_1990': slopes_1975_1990, 
        'Slope_1990_2004': slopes_1990_2004,
        'Slope_2005_2019': slopes_2005_2019
    })

    # Determine whether each county had an overall increase or decrease in each period
    slopes_df['Trend_prior_1975'] = np.where(slopes_df['Slope_prior_1975'] > 0, 'Increase', 'Decrease')
    slopes_df['Trend_1975_1990'] = np.where(slopes_df['Slope_1975_1990'] > 0, 'Increase', 'Decrease')
    slopes_df['Trend_1990_2004'] = np.where(slopes_df['Slope_1990_2004'] > 0, 'Increase', 'Decrease')
    slopes_df['Trend_2005_2019'] = np.where(slopes_df['Slope_2005_2019'] > 0, 'Increase', 'Decrease')

    # Resetting the index to make 'CountyName' a column
    slopes_df_reset = slopes_df.reset_index()

    # Melting the DataFrame for plotting with seaborn
    melted_slopes = pd.melt(slopes_df_reset, id_vars='CountyName', value_vars=['Slope_prior_1975', 'Slope_1975_1990','Slope_1990_2004', 'Slope_2005_2019'], var_name='Period', value_name='Slope')
    melted_slopes['Period'] = melted_slopes['Period'].replace({'Slope_prior_1975': 'Prior to 1975', 'Slope_1975_1990': '1975 to 1989', 'Slope_1990_2004': '1990 to 2004', 'Slope_2005_2019': '2005 to 2019'})
    melted_trends = pd.melt(slopes_df_reset, id_vars='CountyName', value_vars=['Trend_prior_1975', 'Trend_1975_1990', 'Trend_1990_2004', 'Trend_2005_2019'], var_name='Period', value_name='Trend')
    melted_trends['Period'] = melted_trends['Period'].replace({'Trend_prior_1975':'Prior to 1975', 'Trend_1975_1990': '1975 to 1989','Trend_1990_2004': '1990 to 2004', 'Trend_2005_2019': '2005 to 2019'})

    # Merging the melted dataframes
    melted_data = pd.merge(melted_slopes, melted_trends, on=['CountyName', 'Period'])
    # Create the catplot
    g = sns.catplot(data=melted_data, x='Period', y='Slope', hue='Trend', kind='swarm',
                palette={'Increase': '#C8102E', 'Decrease': '#CAC7A7'}, 
                aspect=1.5,  # Makes the plot wider
                height=6)  # Makes the plot taller)
    plt.title('Comparison of Slopes of Commercial Nitrogen Rates Prior and After EISA mandates',  fontsize = 20)
    plt.ylabel('Slope', fontsize = 16)
    plt.xlabel('Period',  fontsize = 16)
    plt.tick_params(axis='both', labelsize=14)

    # Calculate the y position for the annotations
    y_position = plt.ylim()[1] - (plt.ylim()[1] - plt.ylim()[0]) * 0.20

    # Add a vertical line at the transition between time periods
    plt.axvline(2.5, color='gray', linestyle='--', lw=0.7)  # Adding vertical line between 1990 to 2004 and 2005 to 2019

    # Adding annotations with horizontal arrows at 1/4 height from top
    plt.annotate('Before EISA mandate', xy=(2.5, y_position), xytext=(-20, 0),
                textcoords='offset points', ha='right', va='center', color='gray', fontsize = 14, 
                arrowprops=dict(arrowstyle='<-', lw=.5, color='gray'))

    plt.annotate('Post EISA mandate', xy=(2.5, y_position), xytext=(20, 0),
                textcoords='offset points', ha='left', va='center', color='gray', fontsize = 14, 
                arrowprops=dict(arrowstyle='<-', lw=.5, color='gray'))

    fname = os.path.join(parent_dir, "fig11_ns_methods_trends.png")

    plt.tight_layout()
    plt.savefig(fname, dpi='figure', format='png')
    plt.show()

ns_methods_trends(gdf, parent_dir)