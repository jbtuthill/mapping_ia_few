import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable
import pandas as pd
import os

# Set current working directory
current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)
os.chdir(current_directory)

ifews = gpd.read_file(os.path.join(os.path.abspath(os.path.join(current_directory, '../../datasets/')), "IFEWs.geojson"))
ifews['Year'] = pd.to_numeric(ifews['Year'])
parent_dir = os.path.abspath(os.path.join(current_directory, '../vis_png'))

def ns_components_plot(ifews, parent_dir):
    # Create custom colormaps
    cmap_CN = LinearSegmentedColormap.from_list('Yellows', ['#FDF5E3', '#F1BE48'])
    cmap_FN = LinearSegmentedColormap.from_list('Reds', ['#FCE0E5', '#C8102E'])
    cmap_GN = LinearSegmentedColormap.from_list('Greys', ['#F4F3EC', '#9B945F'])
    cmaps = [cmap_CN, cmap_FN, cmap_GN]

    # Function to plot thematic maps on specific axes with optional colorbars, titles, and year labels
    def plot_map_on_ax(gdf, column, title, cmap, ax, vmin, vmax, add_colorbar=False, add_title=False, add_year_label=False, year=None):
        if add_colorbar:
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("bottom", size="5%", pad=0.1)
            mapping = gdf.plot(column=column, cmap=cmap, legend=True, ax=ax, vmin=vmin, vmax=vmax, cax=cax, legend_kwds={'orientation': "horizontal"})
            cax.tick_params(labelsize=40)  # Set font size for colorbar
        else:
            mapping = gdf.plot(column=column, cmap=cmap, legend=False, ax=ax, vmin=vmin, vmax=vmax)
        if add_title:
            ax.set_title(title, fontsize=40)
        ax.axis('off')

        if add_year_label:
            ax.annotate(str(year), xy=(-0.1, 0.5), xycoords='axes fraction', textcoords='offset points',
                        xytext=(0, 0), va='center', ha='right', fontsize=40, rotation=90)

    agg_gdf = ifews.groupby(['CountyName', 'Year']).mean(numeric_only=True).reset_index()
    agg_gdf = gpd.GeoDataFrame(agg_gdf.merge(ifews[['CountyName', 'geometry']].drop_duplicates(), on='CountyName'))

    # Find global vmin and vmax for thematic maps
    vmin_CN, vmax_CN = agg_gdf['CN'].min(), agg_gdf['CN'].max()
    vmin_FN, vmax_FN = agg_gdf['FN'].min(), agg_gdf['FN'].max()
    vmin_GN, vmax_GN = agg_gdf['GN'].min(), agg_gdf['GN'].max()

    vmin = max(vmin_GN, vmin_FN, vmin_CN)
    vmax = max(vmax_GN, vmax_FN, vmax_CN)

    # Representative years for thematic maps
    years = [1970, 1982, 1994, 2006, 2018]
    columns = ['CN', 'FN', 'GN']
    titles = ['Chemical Nitrogen (CN)', 'Fixation Nitrogen (FN)', 'Grain Nitrogen Removal (GN)']

    # Plot maps side by side
    fig, axs = plt.subplots(5, 3, figsize=(35, 30))

    for i, year in enumerate(years):
        year_gdf = agg_gdf[agg_gdf['Year'] == year]
        for j, (col, cmap, title) in enumerate(zip(columns, cmaps, titles)):
            add_colorbar = (i == len(years) - 1)  # Add colorbar only on the last row
            add_title = (i == 0)  # Add titles only on the first row
            add_year_label = (j == 0)  # Add year labels only on the first column
            plot_map_on_ax(year_gdf, col, title, cmap, axs[i, j], vmin, vmax, add_colorbar, add_title, add_year_label, year)
    
    fname = os.path.join(parent_dir, "fig4_spatial_distribution_CN_FN_GN.png")

    plt.tight_layout()
    plt.savefig(fname, dpi='figure', format='png')
    plt.show()

def crop_plot(ifews, parent_dir):
    # Create custom colormaps
    cmap_FN = LinearSegmentedColormap.from_list('Reds', ['#FCE0E5', '#C8102E'])
    cmap_GN = LinearSegmentedColormap.from_list('Grays', ['#F4F3EC', '#9B945F'])

    # Function to plot thematic maps on specific axes with customized colorbars
    def plot_map_on_ax(gdf, column, title, cmap, ax, vmin, vmax):
        # Create the plot with the custom colormap and no initial colorbar
        mapping = gdf.plot(column=column, cmap=cmap, legend=False, ax=ax, vmin=vmin, vmax=vmax, missing_kwds={'color': 'lightgrey'})
        ax.set_title(title, fontsize=30)
        ax.axis('off')
        
        # Create a colorbar with the mapping
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.1)
        cbar = plt.colorbar(mapping.collections[0], cax=cax, orientation='vertical')  # Specify vertical orientation
        cbar.ax.tick_params(labelsize=30)  # Set font size for colorbar labels

    # Aggregate data over time to calculate mean and standard deviation
    agg_mean = ifews.groupby(['CountyName']).mean(numeric_only=True).reset_index()
    agg_std = ifews.groupby(['CountyName']).std(numeric_only=True).reset_index()

    # Merge geometries
    agg_mean = gpd.GeoDataFrame(agg_mean.merge(ifews[['CountyName', 'geometry']].drop_duplicates(), on='CountyName'))
    agg_std = gpd.GeoDataFrame(agg_std.merge(ifews[['CountyName', 'geometry']].drop_duplicates(), on='CountyName'))

    # Find global vmin and vmax for average and standard deviation thematic maps
    vmin_FN_mean, vmax_FN_mean = agg_mean['FN'].min(), agg_mean['FN'].max()
    vmin_GN_mean, vmax_GN_mean = agg_mean['GN'].min(), agg_mean['GN'].max()
    vmin_FN_std, vmax_FN_std = agg_std['FN'].min(), agg_std['FN'].max()
    vmin_GN_std, vmax_GN_std = agg_std['GN'].min(), agg_std['GN'].max()

    # Use consistent min/max for FN and GN in agg_mean and agg_std maps
    vmin_mean = min(vmin_FN_mean, vmin_GN_mean)
    vmax_mean = max(vmax_FN_mean, vmax_GN_mean)
    vmin_std = min(vmin_FN_std, vmin_GN_std)
    vmax_std = max(vmax_FN_std, vmax_GN_std)

    # Plot maps side by side
    fig, axs = plt.subplots(2, 2, figsize=(28, 20))

    # Average values
    plot_map_on_ax(agg_mean, 'FN', 'Average Fixation Nitrogen (FN) in Iowa', cmap_FN, axs[0, 0], vmin_mean, vmax_mean)
    plot_map_on_ax(agg_mean, 'GN', 'Average Grain Nitrogen (GN) in Iowa', cmap_GN, axs[0, 1], vmin_mean, vmax_mean)

    # Standard deviation
    plot_map_on_ax(agg_std, 'FN', 'Standard Deviation of Fixation Nitrogen (FN) in Iowa', cmap_FN, axs[1, 0], vmin_std, vmax_std)
    plot_map_on_ax(agg_std, 'GN', 'Standard Deviation of Grain Nitrogen (GN) in Iowa', cmap_GN, axs[1, 1], vmin_std, vmax_std)

    fname = os.path.join(parent_dir, "fig5_spatial_distribution_FN_GN_average_std_dev.png")

    plt.tight_layout()
    plt.savefig(fname, dpi='figure', format='png')
    plt.show()

ns_components_plot(ifews, parent_dir)
crop_plot(ifews, parent_dir)    