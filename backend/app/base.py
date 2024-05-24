import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

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

#templates = Jinja2Templates(directory='climate_data/json_data')

'''api = Flask(__name__)
api.config.from_object(AppConfig)
api.secret_key = AppConfig.SECRET_KEY

# Set up CORS with specific origins and allow credentials
CORS(api, supports_credentials=True, origins=["http://localhost:3000"])
app_session = Session(api)
socket_io = SocketIO(api, cors_allowed_origins = "http://localhost:3000")'''

DEMO_bird_data = {
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


app.get('/bird-data/{bird_name}')
def get_bird_data(bird_name):
  if bird_name in DEMO_bird_data:
    return DEMO_bird_data
      

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
  bird = DEMO_bird_data.get(bird_name)
  if bird:
    return {
      'name': bird_name,
      'info': bird['info']
    }
  else:
    raise HTTPException(
      status_code= 404,
      detail= f"data for bird {bird_name} does not exist.")
      

@app.get('/bird-sdm-data/{bird_name}')
def get_bird_sdm_data(bird_name):
  bird = DEMO_bird_data.get(bird_name)
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