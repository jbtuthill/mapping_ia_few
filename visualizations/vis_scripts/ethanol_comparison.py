import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import warnings 
warnings.filterwarnings('ignore') 
import os

# Set current working directory
current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)
os.chdir(current_directory)

parent_dir = os.path.abspath(os.path.join(current_directory, '../vis_png'))

# IFEWs data
results = pd.read_csv(os.path.join(os.path.abspath(os.path.join(current_directory, '../../datasets/')), "MinimizeSSE_resultsforplot.csv"))

def ethanol_comp(results, parent_dir):
 
    fig, ax = plt.subplots()

    ax.scatter(results['Year'], results['IA_Thousand barrels'],  color='#C8102E', s = 10, zorder=1, label = 'EIA Report')
    ax.scatter(results['Year'], results['Ethanol IFEWs (Thousands of Barrels)'], color='#F1BE48', s = 10, zorder=1, alpha = 0.7, label = 'Equation 6 Results')

    # Add the legend outside of the subplots
    ax.legend(bbox_to_anchor=(0.05, 1), loc='upper left')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.ylabel('Thousands of Barrels', fontsize = 9)
    plt.xlabel('Year', fontsize = 9)

    plt.title('Ethanol Production')

    fname = os.path.join(parent_dir, "fig12_ethanol_comp.png")

    plt.tight_layout()
    plt.savefig(fname, dpi='figure', format='png')
    plt.show()

ethanol_comp(results, parent_dir)

