import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

import requests
import json

import os

#from .config import AppConfig
import pandas as pd
import numpy as np
from shapely.geometry import LineString

from PIL import Image
from io import BytesIO
import base64
# DEBUGGING
import sys
from time import sleep

app = FastAPI()
frontend_origin = "http://localhost:3000"
app.add_middleware(
  CORSMiddleware,
  allow_origins= frontend_origin,
  allow_credentials= True,
  allow_methods=["*"],
  allow_headers=["*"])


bird_data = {
  "Blackpoll Warbler": {
    "info": "Migration details about Blackpoll Warbler",
    "sdmData": [{"x": 1, "y": 300}, {"x": 2, "y": 600}, {"x": 3, "y": 800}],
    "timeSeriesData": {
        "precipitation": [300, 400, 500],
        "climate": [30, 40, 50],
        "temperature": [60, 70, 80],
    },
  },
  "Bald Eagle": {
    "info": "Migration details about Bald Eagle",
    "sdmData": [{"x": 1, "y": 100}, {"x": 2, "y": 200}, {"x": 3, "y": 500}],
  },
  "White Fronted Goose": {
    "info": "Migration details about White Fronted Goose",
    "sdmData": [{"x": 1, "y": 300}, {"x": 2, "y": 600}, {"x": 3, "y": 800}],
  },
  "Long Billed Curlew": {
    "info": "Migration details about Long Billed Curlew",
    "sdmData": [{"x": 1, "y": 300}, {"x": 2, "y": 600}, {"x": 3, "y": 800}],
  },
  "Whimbrel": {
    "info": "Migration details about Whimbrel",
    "sdmData": [{"x": 1, "y": 300}, {"x": 2, "y": 600}, {"x": 3, "y": 800}],
  },
}

bird_information_data = {
    "Blackpoll Warbler": {
        "general": "The blackpoll warbler (Setophaga striata) is a New World warbler. Breeding males are mostly black and white. They have a prominent black cap, white cheeks, and white wing bars. The blackpoll breeds in forests of northern North America, from Alaska throughout most of Canada, to the Adirondack Mountains of New York as well as New England in the Northeastern United States. They are a common migrant throughout much of North America. In fall, they fly south to the Greater Antilles and the northeastern coasts of South America in a non-stop long-distance migration over open water, averaging 2,500 km (1,600 mi), one of the longest-distance non-stop overwater flights ever recorded for a migratory songbird. Rare vagrants to western Europe, they are one of the more frequent transatlantic passerine wanderers.",
        "migration" : "Blackpoll warblers have the longest migration of any species of New World warbler. This is likely the reason that they are one of the later warblers to appear in spring migration, after one or more short overwater flights and a relatively prolonged movement overland through North America anytime from early May to mid-June. The peak of their migration is in late May when most warblers are on their breeding grounds. In the fall, the birds migrate from their breeding grounds across the northern latitudes. They converge on the Northeastern United States south to Virginia starting in mid-August. Most blackpolls fly directly from northeastern North America over the Atlantic Ocean to their winter range. Data from nocturnal accidents, banding stations, and sightings have shown that blackpolls are rare autumn migrants south of Cape Hatteras, North Carolina, whereas north of Cape Hatteras they are common.[10] Part of the fall migratory route of the blackpoll warbler is over the Atlantic Ocean from the northeastern United States to the Greater and Lesser Antilles or northern South America. Island stopovers at Bermuda and other places are evidence of migratory pathways.[11] To accomplish this flight, the blackpoll warbler nearly doubles its body mass in staging areas and takes advantage of a shift in prevailing wind direction to direct it to its destination. When they fly southward over the Atlantic, they burn 0.08 g of fat every hour. This route averages 3,000 km (1,900 mi) over water, requiring a potentially nonstop flight of around 72 to 88 hours. They travel at a speed of about 27 mph (43 km/h). Blackpolls can weigh more than 20 g (0.71 oz) when they leave the United States and lose 4 or more grams by the time they reach South America. Some of the blackpolls land in Bermuda before going on.",
        "source": "https://en.wikipedia.org/wiki/Blackpoll_warbler",
    },
    "Bald Eagle" : {
        "general": "The bald eagle (Haliaeetus leucocephalus) is a bird of prey found in North America. A sea eagle, it has two known subspecies and forms a species pair with the white-tailed eagle (Haliaeetus albicilla), which occupies the same niche as the bald eagle in the Palearctic.",
        "migration": "The majority of bald eagles in Canada are found along the British Columbia coast while large populations are found in the forests of Alberta, Saskatchewan, Manitoba and Ontario. Bald eagles also congregate in certain locations in winter. From November until February, one to two thousand birds winter in Squamish, British Columbia, about halfway between Vancouver and Whistler. In March 2024, bald eagles were found nesting in Toronto for the first time.[39] The birds primarily gather along the Squamish and Cheakamus Rivers, attracted by the salmon spawning in the area. Similar congregations of wintering bald eagles at open lakes and rivers, wherein fish are readily available for hunting or scavenging, are observed in the northern United States.  Its range includes most of Canada and Alaska, all of the contiguous United States, and northern Mexico. It is found near large bodies of open water with an abundant food supply and old-growth trees for nesting. Bald eagles are not bald; the name derives from an older meaning of the word, \"white headed\". The adult is mainly brown with a white head and tail. The sexes are identical in plumage, but females are about 25 percent larger than males. The yellow beak is large and hooked. The plumage of the immature is brown. The bald eagle is the national bird of the United States of America and appears on its seal. In the late 20th century it was on the brink of extirpation in the contiguous United States. Populations have since recovered, and the species's status was upgraded from \"endangered\" to \"threatened\" in 1995, and removed from the list altogether in 2007. It is partially migratory, depending on location. If its territory has access to open water, it remains there year-round, but if the body of water freezes during the winter, making it impossible to obtain food, it migrates to the south or to the coast. The bald eagle selects migration routes which take advantage of thermals, updrafts, and food resources. During migration, it may ascend in a thermal and then glide down, or may ascend in updrafts created by the wind against a cliff or other terrain. Migration generally takes place during the daytime, usually between the local hours of 8:00 a.m. and 6:00 p.m., when thermals are produced by the sun.",
        "source": "https://en.wikipedia.org/wiki/Bald_eagle",
    },
    "White Fronted Goose" : {
        "general": "The greater white-fronted goose (Anser albifrons) is a species of goose that is closely related to the smaller lesser white-fronted goose (A. erythropus). The greater white-fronted goose is migratory, breeding in northern Canada, Alaska, Greenland and Russia, and winters farther south in North America, Europe and Asia. It is named for the patch of white feathers bordering the base of its bill: albifrons comes from the Latin albus \"white\" and frons \"forehead\". In the United Kingdom and Ireland, it has been known as the white-fronted goose; in North America it is known as the greater white-fronted goose (or \"greater whitefront\"), and this name is also increasingly adopted internationally. Even more distinctive are the salt-and-pepper markings on the breast of adult birds, which is why the goose is colloquially called the \"specklebelly\" in North America.",
        "migration": "The Pacific white-fronted goose migrate south down the Pacific coast, staging primarily in the Klamath Basin of southern Oregon and northern California and wintering, eventually, in California's Central Valley. The tule goose is somewhat rare and has been since the latter half of the 19th century, presumably it was affected by destruction of its wintering habitat due to human settlement.",
        "source": "https://en.wikipedia.org/wiki/Greater_white-fronted_goose",
    },
    "Long Billed Curlew": {
        "general": "The long-billed curlew (Numenius americanus) is a large North American shorebird of the family Scolopacidae. This species was also called \"sicklebird\" and the \"candlestick bird\". The species breeds in central and western North America, migrating southward and coastward for the winter.",
        "migration": "",
        "source": "https://en.wikipedia.org/wiki/Long-billed_curlew",
    },
    "Whimbrel" : {
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


app.get('/bird-data/{bird_name}')
def get_bird_data(bird_name):
  if bird_name in bird_data:
    return bird_data
      

class PredictionInputs(BaseModel):
  bird: str
  year: int
  emissions: str
    
@app.put('/prediction')
async def predict(prediction_input: PredictionInputs):
  selected_bird = prediction_input.bird
  selected_year = str(prediction_input.year)
  emission_Type = prediction_input.emissions
    
  '''
  # Store the inputs into a session, cached for future utility
  session['bird'] = input_bird#prediction_input['bird']
  session['year'] = input_year#prediction_input['year']
  session['emissions'] = input_emission#prediction_input['emissions']'''
  
  birdsModelDirs = {
    "warbler": "Setophaga_striata",
    "eagle": "Haliaeetus_leucocephalus",
    "anser": "Anser_albifrons",
    "curlew": "Numenius_americanus",
    "whimbrel": "Numenius_phaeopus"
  }
  
  # For image data:
  output_path = f"../../model/outputs/png-images/{birdsModelDirs[selected_bird]}/{emission_Type}/{selected_year}.png"
  dataImg = Image.open(output_path)
  buffer = BytesIO()
  dataImg.save(buffer, format="png")
  
  # Artificial delay to simulate model prediction time
  #sleep(2.5)
  
  #If we'll need to encapsulate a file, use this:
  return {
    "prediction": base64.b64encode(buffer.getvalue()).decode(),
    "resFormat": dataImg.format
  }
    

@app.get('/bird-info/{bird_name}')
def get_bird_info(bird_name):
  bird = bird_information_data.get(bird_name)
  if bird:
    return {
        'general': bird["general"],
        'migration': bird["migration"]
    }
  else:
    raise HTTPException(
      status_code= 404,
      detail= f"data for bird {bird_name} does not exist.")
      

@app.get('/bird-sdm-data/{bird_name}')
def get_bird_sdm_data(bird_name):
  bird = bird_data.get(bird_name)
  if bird:
    return {
      'name': bird_name,
      'sdmData': bird['sdmData']
    }
  else:
    raise HTTPException(status_code=404, detail='Bird not found')

    
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
        details= 'No trajectory data found for given bird ID')

    # Convert data to dictionary format
    trajectory_data = bird_data[['LATITUDE', 'LONGITUDE', 'TIMESTAMP']].to_dict(orient='records')
    return trajectory_data
  except FileNotFoundError:
    raise HTTPException(
      status_code= 404,
      details= f'CSV file for {bird} not found')
        

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
      detail= f'CSV file for {bird} not found')


@app.get('/get_general_migration')
def get_general_migration(selected_bird: str):
  filename = f'./data/{selected_bird}.csv'
  
  try:
    df = pd.read_csv(filename, low_memory=False)
    
    # Convert TIMESTAMP column to datetime
    df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'])
    
    # Group by ID and get the start and end months for each group
    grouped = df.groupby('ID')
    print(grouped)
    simplified_polylines = []
    for _, group in grouped:
      # Sort by timestamp
      group = group.sort_values(by='TIMESTAMP')
      
      # Get coordinates
      coordinates = list(zip(group['LATITUDE'], group['LONGITUDE']))
      
      # Apply Douglas-Peucker algorithm for simplification
      simplified_line = simplify_line(coordinates)
      
      # Calculate direction for simplified line
      start_point = simplified_line[0]
      end_point = simplified_line[-1]
      delta_lat = end_point[0] - start_point[0]
      delta_lon = end_point[1] - start_point[1]
      direction = np.arctan2(delta_lat, delta_lon) * (180 / np.pi)
      
      # Append simplified line with direction to simplified_polylines
      simplified_polylines.append({
          'coordinates': simplified_line,
          'direction': direction
      })
    
    return {'segmented_polylines': simplified_polylines}
  
  except Exception as e:
    raise HTTPException(status_code= 400, detail=str(e))

        
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

    
'''if __name__ == '__main__':
    uvicorn.run(app, port= 8000)
    #api.run(debug=True)
    #socket_io.run(api, debug=True, port=8000)
'''