# Datasets for IFEWs Data Processing

This folder contains the datasets used and/or generated by the scripts in the study "Mapping the Nexus: A County-Level Analysis and Visualization of Iowa's Food-Energy-Water Systems." The datasets are organized into subfolders based on their purpose and origin.

## Folder Structure

### 1. `Iowa Counties`
This folder contains the shapefiles representing the boundaries of counties in Iowa. These files are used as the base for spatial data processing and visualization.

**Files:**
- `Counties.CountyName.atx`
- `Counties.cpg`
- `Counties.dbf`
- `Counties.prj`
- `Counties.sbn`
- `Counties.sbx`
- `Counties.shp`
- `Counties.shp.xml`
- `Counties.shx`
- `IowaCounties.cpg`
- `IowaCounties.dbf`
- `IowaCounties.prj`
- `IowaCounties.shp`
- `IowaCounties.shx`
- `Iowa_County_Boundaries.geojson`

### 2. `N fertilizer data_Iowa`
This folder contains the output of the `nrate` function from the `caopeiyu_nrate.py` script. Each file represents nitrogen rate data for a specific year, aggregated to county-level GeoJSON files.

**Files:**
- `Nrate_1968.geojson`
- `Nrate_1969.geojson`
- `Nrate_1970.geojson`
- ...
- `Nrate_2019.geojson`

### 3. `N fertilizer maps US from 2022`
This folder contains data from another researcher, which is not included in the repository due to its size and external availability. The data can be accessed from [PANGAEA](https://doi.pangaea.de/10.1594/PANGAEA.883585).

**Note:** This folder is not available here. For access to data use the above link.

### 4. IFEWs.rar > `IFEWs.geojson`
This file contains the final integrated dataset with nitrogen surplus calculations and other related data. The CRS (Coordinate Reference System) information for this file is as follows:

**CRS Info:**
- **Name:** WGS 84 / Pseudo-Mercator
- **Axis Info [cartesian]:**
  - X[east]: Easting (metre)
  - Y[north]: Northing (metre)
- **Area of Use:**
  - name: World between 85.06°S and 85.06°N.
  - bounds: (-180.0, -85.06, 180.0, 85.06)
- **Coordinate Operation:**
  - name: Popular Visualisation Pseudo-Mercator
  - method: Popular Visualisation Pseudo Mercator
- **Datum:** World Geodetic System 1984 ensemble
  - Ellipsoid: WGS 84
  - Prime Meridian: Greenwich

### 5. CornRates
This folder contains the data and results from processing Corn Rates. The subfolders CDL_tifs and GJSON are included in the .gitignore file due to their size and the external availability of the source data.

### 6. manure.rar >`manure.geojson`
This file contains the county scale manure dataset from Bian et al. (https://doi.pangaea.de/10.1594/PANGAEA.919937)

### 7. MinimizeSSE_resultsforplot.csv
This file includes the results from the MinimizeSSE.xlsx file located in the scripts folder. It contains data used for plotting and analysis of the ethanol production model.

### 8. Ethanol
This folder contains supporting data used in the MinimizeSSE.xlsx file for the ethanol analysis. All include ERS USDA data and sources for EIA data.

Folders:

- CDL_tifs: Contains Cropland Data Layer (CDL) TIFF files (available at https://croplandcros.scinet.usda.gov/)
- GJSON: Contains GeoJSON files generated from the CDL TIFF files and state crop rate data.

Workflow:
The CornRates processing involves converting JSON files to features, overlaying layers, calculating geometry attributes, selecting layers by attributes, summarizing statistics, adding joins, calculating fields, and exporting features to GeoJSON files. The steps are detailed in the provided ModelBuilder script, which outlines the entire workflow for generating the GeoJSON files.
