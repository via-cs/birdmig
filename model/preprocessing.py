import geopandas as gpd
import pandas as pd
import os
import sys

filename = sys.argv[1]
if not filename.endswith('.csv'):
    sys.exit("Error: argument must be a valid .csv file")

dest_file = filename.replace('.csv', '.shp')

df = pd.read_csv(filename, sep='\t', lineterminator='\n')

# Get the list of all column names from headers
use_cols = ['occurrenceID', 'basisOfRecord', 'eventDate', 'kingdom', 'scientificName', 'taxonRank', 'decimalLatitude', 'decimalLongitude', 'countryCode', 'individualCount']
df_trim = df[use_cols]

# Rename for shapefile 10 character header limit
df_shp = df_trim.rename(columns={'occurrenceID': 'occID', 'basisOfRecord': 'basis', 'scientificName' : 'sciName', 'decimalLatitude' : 'lat', 'decimalLongitude' : 'lon', 'countryCode' : 'country', 'individualCount' : 'indivCount'})

# Create geopanda dataframe
pa = gpd.GeoDataFrame(df_shp, 
    geometry = gpd.points_from_xy(df_shp['lat'], df_shp['lon']), 
    crs = 'EPSG:4326')

# Remove duplicates
species_distribution_unique = pa.drop_duplicates(subset=['geometry'])
species_distribution_unique.reset_index(drop=True, inplace=True)

# Export file
species_distribution_unique.to_file(dest_file, driver='ESRI Shapefile')