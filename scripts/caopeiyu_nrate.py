import os
import numpy as np
from shapely.geometry import mapping
import rioxarray as rxr
import geopandas as gpd
import rasterio
from rasterstats import zonal_stats
import pandas as pd

def nrate_original(parent_dir):
    """
    Process original nitrogen fertilizer data from rasters to points and aggregate to counties.
    
    Parameters:
    - parent_dir (str): Directory path containing the dataset files.
    """
    dir_name1 = os.path.join(parent_dir, "N fertilizer maps US from 2022")
    files = os.listdir(dir_name1)

    # Filter files: select only .tif files for years >= 1968
    files = [x for x in files if "N fertilizer data" not in x and x.endswith(".tif")]
    y = [str(i) for i in range(1900, 1968)]
    for year in y:
        files = [x for x in files if year not in x]

    # Get boundary data
    file_boundary = os.path.join(parent_dir, "Iowa Counties", 'IowaCounties.shp')

    for idx, file in enumerate(files):
        iowa = gpd.read_file(file_boundary)
        year = 1968 + idx
        f = os.path.join(dir_name1, file)

        # Open and clip raster
        fertilizer_im = rxr.open_rasterio(f, masked=True).squeeze()
        nrate_clipped = fertilizer_im.rio.clip(iowa.geometry.apply(mapping), iowa.crs)

        # Export clipped raster
        path_to_tif_file = os.path.join(dir_name1, 'N fertilizer data_Iowa', file)
        nrate_clipped.rio.to_raster(path_to_tif_file)

        # Convert raster to points
        with rasterio.open(path_to_tif_file) as src:
            data = src.read(1, masked=True)
            if not data.mask.all():
                meta = src.meta
                points = np.where(data.mask == False)
                if len(points) == 1:
                    lon, lat = src.xy(points[0], np.zeros_like(points[0]))
                else:
                    lon, lat = src.xy(points[0], points[1])
                df = pd.DataFrame({'Longitude': lon, 'Latitude': lat})
                geometry = gpd.points_from_xy(df.Longitude, df.Latitude)
                crs = src.crs
                point_gdf = gpd.GeoDataFrame(df, crs=crs, geometry=geometry)
        
        iowa1 = iowa.to_crs(fertilizer_im.rio.crs)
        stats = zonal_stats(iowa1, path_to_tif_file, stats='mean', nodata=-999)
        mean_vals = [feature['mean'] for feature in stats]
        iowa['CN_lb/ac'] = mean_vals
        iowa['date'] = year

        iowa_utm = iowa.to_crs(epsg=26915)
        iowa = iowa.drop(['FID', 'PERIMETER', 'DOMCountyI', 'FIPS', 'FIPS_INT', 'SHAPE_Leng', 'SHAPE_Area'], axis=1)

        path_to_geojson_file = os.path.join(parent_dir, 'N fertilizer data_Iowa', f"Nrate_{year}.geojson")
        iowa_utm.to_file(path_to_geojson_file)

def nrate(current_directory):
    """
    Aggregate individual GeoJSON files into a single temporal series GeoDataFrame.
    
    Parameters:
    - current_directory (str): Directory path containing the script files.
    
    Returns:
    - nrate_gdf (GeoDataFrame): Aggregated GeoDataFrame with nitrogen rate data.
    """
    parent_dir = os.path.abspath(os.path.join(current_directory, '../datasets'))
    # run if initial dataset is updated.
    # nrate_original(parent_dir=parent_dir)

    dir_name2 = os.path.join(parent_dir, "N fertilizer data_Iowa")
    files = [x for x in os.listdir(dir_name2) if x.endswith(".geojson")]

    filepaths = [os.path.join(dir_name2, file) for file in files]
    gdfs = [gpd.read_file(filepath) for filepath in filepaths]

    nrate_gdf = pd.concat(gdfs, ignore_index=True)

    nrate_gdf['date'] = pd.to_datetime(nrate_gdf['date'], format='%Y')
    nrate_gdf['Year'] = nrate_gdf['date'].dt.year

    nrate_gdf = nrate_gdf.drop(['FID', 'PERIMETER', 'DOMCountyI', 'FIPS', 'FIPS_INT', 'SHAPE_Leng', 'SHAPE_Area', 'date'], axis=1)
    nrate_gdf.rename(columns={"StateAbbr": "State"}, inplace=True)
    nrate_gdf['CountyName'] = nrate_gdf['CountyName'].replace('Obrien', "O BRIEN")
    nrate_gdf['CountyName'] = nrate_gdf['CountyName'].str.upper()

    return nrate_gdf