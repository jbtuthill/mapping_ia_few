import matplotlib.pyplot as plt
import geopandas as gpd
import warnings 
warnings.filterwarnings('ignore') 
import os

# Set current working directory
current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)
os.chdir(current_directory)

# IFEWs data
gdf = gpd.read_file(os.path.join(os.path.abspath(os.path.join(current_directory, '../../datasets/')), "IFEWs.geojson"))
gdf['Year'] = gdf['Year'].astype(int)
gdf = gdf.drop(gdf[gdf['Year'] == 2018].index)
gdf = gdf.drop(gdf[gdf['Year'] == 2019].index)
columns_to_merge = ['Year', 'CountyName', 'MN', 'MN_old']
gdf_subset = gdf[columns_to_merge]

# Manure from Bian et al.
merged_df = gpd.read_file(os.path.join(os.path.abspath(os.path.join(current_directory, '../../datasets/')), "manure.geojson"))
merged_gdf = gdf_subset.merge(merged_df, on=['Year', 'CountyName'], how='left')
merged_gdf['diff'] = merged_gdf['MN'] - merged_gdf['mean_Pro_kgNha']     
merged_gdf['diff_old'] = merged_gdf['MN_old'] - merged_gdf['mean_Pro_kgNha'] 

parent_dir = os.path.abspath(os.path.join(current_directory, '../vis_png'))

# Descriptive Statistics
diff_stats = merged_gdf['diff'].describe()

def manure_methods_comparison(merged_gdf):

    data = [merged_gdf['MN_old'], merged_gdf['MN'], merged_gdf['mean_Pro_kgNha']]

    axis_font_size = 14*1.5  
    title_font_size = 16*1.5  
   
    plt.figure(figsize=(18, 6))
    box = plt.boxplot(data, patch_artist=True,
                    labels=['Manure Nitrogen without \n Storage Loss', 'Manure Nitrogen wtih \n Storage Loss', 'Manure Nitrogen Production \n from Bian et al. (2021)'],
                    boxprops=dict(linewidth=0.7, color = '#9B945F'),
                    whiskerprops=dict(linewidth=0.7, color = '#9B945F'),
                    capprops=dict(linewidth=0.7, color = '#9B945F'),
                    medianprops=dict(linewidth=0.5, color='#C8102E'),
                    showfliers=False)

    color = '#F1BE48'
    for patch in box['boxes']:
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    plt.tick_params(axis='both', labelsize=axis_font_size )
    plt.ylabel('Manure Nitrogen (kg/ha)', fontsize=axis_font_size)
    plt.title('Comparison of Manure Nitrogen Methods', fontsize=title_font_size)
    plt.grid(False)
  
    fname = os.path.join(parent_dir, "fig8_manure_methods.png")

    plt.tight_layout()
    plt.savefig(fname, dpi='figure', format='png')
    plt.show()

manure_methods_comparison(merged_gdf)