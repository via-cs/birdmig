import os
import rasterio
import json
from pathlib import Path

print("Current Working Directory:", os.getcwd())

# Define the directory where the tif files are located (adjust the path as necessary)
tif_files_dir = Path('./tif_files/')  # Potentially adjust this path
json_data_dir = Path('./json_data/')  # Directory to save the JSON files

# Create the directory to save JSON files if it doesn't exist
json_data_dir.mkdir(parents=True, exist_ok=True)

# Verify the existence of the tif_files directory
if not tif_files_dir.exists():
    print(f"Directory not found: {tif_files_dir}")
else:
    # Loop over each subdirectory in the tif_files directory
    for variable_dir in os.listdir(tif_files_dir):
        variable_path = tif_files_dir / variable_dir
        if variable_path.is_dir():
            # List all .tif files in the directory
            tif_files = sorted([f for f in variable_path.glob('*.tif')])
            
            # Initialize an empty list to hold the data
            time_series_data_list = []
            
            # Loop over each .tif file
            for tif_file in tif_files:
                month = int(tif_file.stem.split('_')[-1])  # Assuming filename format includes month at the end
                
                # Open the .tif file
                with rasterio.open(tif_file) as src:
                    # Read the data for the entire .tif file
                    data = src.read(1)
                    
                    # Flatten the array and filter out invalid values
                    valid_data = data.flatten()
                    valid_data = valid_data[~src.dataset_mask().flatten() == 0]  # Mask out the nodata cells
                    valid_data = valid_data[valid_data < 1e30]  # Filter out extreme values
                    
                    # Calculate the mean and convert it to a Python float if not NaN
                    if valid_data.size > 0:
                        mean_value = float(valid_data.mean())
                    else:
                        mean_value = float('nan')

                    # Append the data to the list
                    time_series_data_list.append({'Month': month, 'Mean_Value': mean_value})

            
            # Save the collected data to a JSON file
            json_file_path = json_data_dir / f'{variable_dir}.json'
            with json_file_path.open('w') as json_file:
                json.dump(time_series_data_list, json_file)
