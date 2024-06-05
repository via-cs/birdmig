from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

import requests
import json

import os

import pandas as pd
import numpy as np
from shapely.geometry import LineString
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

from PIL import Image
from io import BytesIO
import base64

app = FastAPI()
frontend_origin = "http://localhost:3000"
app.add_middleware(
  CORSMiddleware,
  allow_origins= frontend_origin,
  allow_credentials= True,
  allow_methods=["*"],
  allow_headers=["*"])


birdsModelDirs = {
    "warbler": "Setophaga_striata",
    "eagle": "Haliaeetus_leucocephalus",
    "anser": "Anser_albifrons",
    "curlew": "Numenius_americanus",
    "whimbrel": "Numenius_phaeopus"
}

bird_information_data = {
    "Blackpoll Warbler": {
      "scientific_name" : "Setophaga Striata",
      "general": "The Blackpoll Warbler, named for the male's black forehead and crown, has the longest migration of any North American warbler. Each fall, most Blackpolls migrate more than 2,000 miles across open water without stopping, sometimes flying for more than 80 hours straight until they reach their Amazon wintering grounds.",
      "migration": "Blackpolls have an “elliptical” migration, traveling a different route in the fall and in the spring. Other birds known to have an elliptical migration pattern include the American Golden-Plover and the Connecticut Warbler, which is the only other North American warbler species known to winter in the Amazonian lowlands. As in many of their tribe, including the Chestnut-sided and Bay-breasted Warblers, male Blackpoll Warblers sport much more subdued coloration as they head south in fall. Gone is the distinctive white cheek and black cap.",
      "source": "https://abcbirds.org/bird/blackpoll-warbler/",
    },
    "Bald Eagle" : {
      "scientific_name": "Haliaeetus Leucocephalus",
      "general": "The majestic Bald Eagle is the only eagle species found solely in North America.The Bald Eagle's Latin name accurately reflects its appearance and habits: Hali and aiētos mean “sea eagle,” and leuco and cephalos mean “white head.” The use of the word \"Bald\" in its English name does not mean hairless; rather, it derives from the Middle English word “balde,” which means shining white.",
      "migration": "The Bald Eagle is a North American specialty, found from Alaska through Canada into the lower 48 U.S. states, even moving as far south as northern Mexico during the winter. It is considered a partial migrant — individuals in the northern parts of the range often move south during extremely cold weather, as this species needs open water to hunt.",
      "source": "https://abcbirds.org/bird/bald-eagle/",
    },
    "White Fronted Goose" : {
      "scientific_name": "Anser Albifrons",
      "general": "The greater white-fronted goose is a species of goose related to the smaller lesser white-fronted goose. It is named for the patch of white feathers bordering the base of its bill, in fact albifrons comes from the Latin albus \"white\" and frons \"forehead\". In Europe it has been known as the white-fronted goose; in North America it is known as the greater white-fronted goose, and this name is also increasingly adopted internationally. Even more distinctive are the salt-and-pepper markings on the breast of adult birds, which is why the goose is colloquially called the \"specklebelly\" in North America.",
      "migration": "The Pacific white-fronted goose migrate south down the Pacific coast, staging primarily in the Klamath Basin of southern Oregon and northern California and wintering, eventually, in California's Central Valley. The tule goose is somewhat rare and has been since the latter half of the 19th century, presumably it was affected by destruction of its wintering habitat due to human settlement.",
      "source": "https://en.wikipedia.org/wiki/Greater_white-fronted_goose",
    },
    "Long Billed Curlew": {
      "scientific_name": "Numenius Americanus",
      "general": "The eye-catching Long-billed Curlew is North America's largest shorebird, but like the Mountain Plover and Buff-breasted Sandpiper, it's very often found away from the shore. Its genus Numenius is named from the Greek word noumenios, meaning “of the new moon” — bestowed upon curlews because their long, curved bills were thought to resemble a sickle-shaped new moon. The birds' lengthy bills, longest in females, also engendered some interesting folk names such as \"sicklebird,\" \"old smoker,\" and \"candlestick bird.\"",
      "migration": "This species is a short- to medium-distance migrant, moving south in flocks to winter along the U.S. West Coast, south into Mexico, Guatemala, and Honduras. Small numbers winter in Florida and along the southeastern Atlantic shore.",
      "source": "https://abcbirds.org/bird/long-billed-curlew/",
    },
    "Whimbrel" : {
      "scientific_name": "Numenius Phaeopus",
      "general": "The Eurasian or common whimbrel (Numenius phaeopus), also known as the white-rumped whimbrel in North America, is a wader in the large family Scolopacidae. It is one of the most widespread of the curlews, breeding across much of subarctic Asia and Europe as far south as Scotland. This species and the Hudsonian whimbrel have recently been split, although some taxonomic authorities still consider them to be conspecific.",
      "migration": "The whimbrel is a migratory bird, wintering on coasts in southern North America and South America. It is also a coastal bird during migration. It is fairly gregarious outside the breeding season.",
      "source" : "https://en.wikipedia.org/wiki/Hudsonian_whimbrel",
    }

}

@app.get('/temperature/{selectedYear}')
def get_temperature_data(selectedYear: int):
    
    # Set parameters
    start = f"{selectedYear}-01-01"
    end = f"{selectedYear}-12-31"

    # Set base URL, and pull the json data down using requests
    base_url = 'http://grid2.rcc-acis.org/GridData'
    input_dict = {
        "state": "CA", "grid": "loca:wmean:rcp85",
        "sdate": start, "edate": end,
        "elems": [{
            "name": "avgt", "interval": "mly", "duration": "mly", "reduce": "mean", "area_reduce": "state_mean"
        }]
    }

    # Attempt to fetch data with error handling
    try:
        response = requests.post(base_url, json=input_dict)
        response.raise_for_status()  # Raise an HTTPError for bad requests (4XX, 5XX)
        rawjson = response.content
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        raise HTTPException(
            status_code= 500,
            detail= "Failed to retrieve data")

    # Load JSON data
    try:
        newdata = json.loads(rawjson)['data']
    except json.JSONDecodeError as e:
        print('JSON Decode Error:', e)
        raise HTTPException(
            status_code= 500,
            detail= "Failed to parse JSON")

    # Convert the JSON data into a dataframe
    final = pd.DataFrame()
    for entry in newdata:
        month_data = pd.DataFrame(entry[1], index=['avgt']).transpose()
        month_data.insert(0, 'month', entry[0])
        month_data = month_data.reset_index().rename(columns={'index': 'county'})
        month_data['year'] = selectedYear
        final = pd.concat([final, month_data])

    # Group by month and calculate average temperature
    monthly_avg = final.groupby('month').agg({'avgt': 'mean'}).reset_index()
    monthly_avg['year'] = selectedYear

    # Convert the aggregated data to a dictionary and return it
    return monthly_avg.to_dict(orient='records')


@app.get('/precipitation/{selectedYear}')
def get_precipitation_data(selectedYear: int):
    start = f"{selectedYear}-01-01"
    end = f"{selectedYear}-12-31"
    base_url = 'http://grid2.rcc-acis.org/GridData'
    input_dict = {
        "state": "CA", "grid": "loca:wmean:rcp85",
        "sdate": start, "edate": end,
        "elems": [{
            "name": "pcpn", "interval": [0, 1], "duration": "mly", "reduce": "sum", "area_reduce": "state_mean"
        }]
    }

    try:
        response = requests.post(base_url, json=input_dict)
        response.raise_for_status()
        rawjson = response.json()  # directly parse JSON here
    except requests.HTTPError as e:
        raise HTTPException(
            status_code=500,
            headers= {"error": "HTTP error"},
            detail= str(e))
        
    except requests.RequestException as e:
        raise HTTPException(
            status_code= 500,
            headers= {"error": "Request failed"},
            detail= str(e))
        
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code= 500,
            headers= {"error": "Failed to parse JSON"},
            detail= str(e))

    # Check if data is empty or not found
    if not rawjson.get('data'):
        raise HTTPException(
            status_code= 404,
            detail= {"error": "No data found for specified parameters"})

    # Process and return data
    final = pd.DataFrame()
    for entry in rawjson['data']:
        month_data = pd.DataFrame(entry[1], index=['pcpn']).transpose()
        month_data.insert(0, 'month', entry[0])
        month_data['year'] = selectedYear
        final = pd.concat([final, month_data])

    # Group by month and calculate average precipitation
    monthly_avg = final.groupby('month').agg({'pcpn': 'mean'}).reset_index()
    monthly_avg['year'] = selectedYear
    return monthly_avg.to_dict(orient='records')


class PredictionInputs(BaseModel):
  bird: str
  year: int
  emissions: str
    
@app.put('/prediction')
async def get_predictions(prediction_input: PredictionInputs):
  selected_bird = prediction_input.bird
  selected_year = str(prediction_input.year)
  emission_Type = prediction_input.emissions
  # For image data:
  output_path = f"../../model/outputs/png-images/{birdsModelDirs[selected_bird]}/{emission_Type}/{selected_year}.png"
  dataImg = Image.open(output_path)
  buffer = BytesIO()
  dataImg.save(buffer, format="png")
  
  # FastAPI requests can handle asynchronous predictions.
  # In practice, this would be waiting for a machine learning model to generate
  # predictions. In this version, waiting wasn't necessary, so it returns immediately.
  
  return {
    "prediction": base64.b64encode(buffer.getvalue()).decode(),
    "resFormat": dataImg.format
  }
    

@app.get('/bird-info/{bird_name}')
def get_bird_info(bird_name):
  bird = bird_information_data.get(bird_name)
  if bird:
    return {
        'scientific_name' : bird["scientific_name"],
        'general': bird["general"],
        'migration': bird["migration"]
    }
  else:
    raise HTTPException(
      status_code= 404,
      detail= f"data for bird {bird_name} does not exist.")
  
  
@app.get('/json/{filename}')
def send_json(filename):
  climate_file_loc = os.path.join('climate_data/json_data', filename)
  if not os.path.exists(climate_file_loc):
    raise HTTPException(
      status_code= 404,
      detail= f"File path for {climate_file_loc} does not exist")
  return FileResponse(climate_file_loc)


@app.get('/get_trajectory_data')
def get_trajectory_data(bird: str, birdID: str):
    
  filename = f'./data/{bird}.csv'
  try:
    df = pd.read_csv(filename)
    df['ID'] = df['ID'].astype(str)
    # Filter data for the specified bird ID
    bird_data = df[df['ID'].str.contains(birdID)]
    if bird_data.empty:
      raise HTTPException(
        status_code= 404,
        detail= 'No trajectory data found for given bird ID')

    # Convert data to dictionary format
    trajectory_data = bird_data[['LATITUDE', 'LONGITUDE', 'TIMESTAMP']].to_dict(orient='records')
    return trajectory_data
  except FileNotFoundError:
    raise HTTPException(
      status_code= 404,
      detail= f'CSV file for {filename} not found')
        

@app.get('/get_bird_ids')
def get_bird_ids(bird: str):
  filename = f'./data/{bird}.csv'
  
  try:
    df = pd.read_csv(filename)
    bird_ids = df['ID'].unique().tolist()
    return bird_ids
  except FileNotFoundError:
    raise HTTPException(
      status_code=404,
      detail= f'CSV file for {filename} not found')

        
def simplify_line(coordinates, tolerance=0.1):
  line = LineString(coordinates)
  simplified_line = line.simplify(tolerance, preserve_topology=False)
  return list(zip(*simplified_line.xy))


@app.get('/get_heatmap_data')
def get_heatmap_data(bird: str):
    filename = f'./data/{bird}.csv'
    try:
        df = pd.read_csv(filename, low_memory=False)
        heatmap_data = df[['LATITUDE', 'LONGITUDE']].values.tolist()
        return heatmap_data
    except Exception as e:
      raise HTTPException(status_code=400, detail= str(e))

source_epsg = 'epsg:4326'  # Input coordinates in EPSG 4326 (WGS84)
target_epsg = 'epsg:3587' 
    
@app.get('/get_SDM_data')
def get_SDM_data(prediction_input: PredictionInputs):
  selected_bird = prediction_input.bird
  selected_year = str(prediction_input.year)
  emission_Type = prediction_input.emissions

  tiff_file_path = f"../model/outputs/tiff-images/{birdsModelDirs[selected_bird]}/{emission_Type}/{selected_year}/probability_1.0.tif"

  with rasterio.open(tiff_file_path) as src:
      # Read the data from the TIFF file
      data = src.read(1)  # Assuming a single band for simplicity

        # Get the transformation parameters for the reprojected image
      transform, width, height = calculate_default_transform(src.crs, target_epsg, src.width, src.height, *src.bounds)

        # Reproject the image
      data_reprojected = np.empty((height, width), dtype=data.dtype)
      reproject(
          source=data,
          destination=data_reprojected,
          src_transform=src.transform,
          src_crs=src.crs,
          dst_transform=transform,
          dst_crs=target_epsg,
          resampling=Resampling.nearest
      )

    # Convert numpy array to list for JSON serialization
  data_list = data_reprojected.tolist()

  # Prepare data to send to frontend
  converted_data = {'data': data_list}

  # Convert data to JSON
  json_data = json.dumps(converted_data)

  # Send converted data to frontend
  return JSONResponse(content=converted_data)
