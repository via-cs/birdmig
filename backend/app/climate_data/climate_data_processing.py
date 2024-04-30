import json
import os
import rasterio
from pathlib import Path
import numpy as np

# Get the directory path of the current script
current_dir = Path(__file__).resolve().parent

# Change the current working directory to the directory containing the script and tif_files directory
os.chdir(current_dir)

# Define the directories for TIF files and JSON data
tif_files_dir = current_dir / 'tif_files'
json_data_dir = current_dir / 'json_data'

# Create the directory to save JSON files if it doesn't exist
json_data_dir.mkdir(parents=True, exist_ok=True)

# List all directories in the tif files directory
variable_dirs = os.listdir(tif_files_dir)

# Loop over each variable directory
for variable_dir in variable_dirs:
    # Define the path to the variable directory
    variable_path = tif_files_dir / variable_dir
    
    # If the variable directory is bio_10 or bio_2.5, skip processing here
    if variable_dir.startswith('bio'):
        continue
    
    # List all TIF files in the variable directory
    tif_files = [f for f in variable_path.glob('*.tif')]
    
    # Initialize an empty list to hold the time series data
    time_series_data_list = []
    
    # Loop over each TIF file
    for tif_file in tif_files:
        # Open the TIF file
        with rasterio.open(tif_file) as src:
            # Read the data as a numpy array
            data = src.read(1)
            
            # Flatten the data array
            flattened_data = data.flatten()
            
            # Remove NaN values from the flattened array
            flattened_data = flattened_data[~np.isnan(flattened_data)]
            
            # Calculate the mean value
            mean_value = np.mean(flattened_data, dtype=np.float64).item()  # Convert to Python float            
            
            # Extract the month from the file name
            month = int(tif_file.stem.split('_')[-1])
            
            # Append the mean value and month to the time series data list
            time_series_data_list.append({'Month': month, 'Mean_Value': mean_value})
    
    # Define the path to save the JSON file
    json_file_path = json_data_dir / f'{variable_dir}.json'
    
    # Write the time series data to a JSON file
    with json_file_path.open('w') as json_file:
        json.dump(time_series_data_list, json_file)

# Process bio variables separately
# Define the different formats for bio variables
bio_formats = ['bio_10', 'bio_2.5']

# Loop over each bio format
for bio_format in bio_formats:
    # Define the directory path for the current bio format
    bio_dir = tif_files_dir / bio_format
    
    # List all TIF files in the bio directory
    tif_files = list(bio_dir.glob('*.tif'))
    
    # Initialize an empty list to hold the time series data
    time_series_data_list = []
    
    # Loop over each TIF file
    for tif_file in tif_files:
        # Open the TIF file
        with rasterio.open(tif_file) as src:
            # Read the data as a numpy array
            data = src.read(1)
            
            # Flatten the data array
            flattened_data = data.flatten()
            
            # Remove NaN values from the flattened array
            flattened_data = flattened_data[~np.isnan(flattened_data)]
            
            # Calculate the mean value
            mean_value = np.mean(flattened_data, dtype=np.float64).item()  # Convert to Python float            
            
            # Extract the variable number from the file name
            variable_number = int(tif_file.stem.split('_')[-1])
            
            # Append the mean value and variable number to the time series data list
            time_series_data_list.append({'Variable': variable_number, 'Mean_Value': mean_value})
    
    # Define the path to save the JSON file for the current bio format
    json_file_path = json_data_dir / f'{bio_format}.json'
    
    # Write the time series data to a JSON file
    with json_file_path.open('w') as json_file:
        json.dump(time_series_data_list, json_file)
