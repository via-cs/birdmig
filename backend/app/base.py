from flask import Flask, jsonify, request, session, send_from_directory
from flask_cors import CORS, cross_origin
from flask_session import Session
from flask_socketio import SocketIO, emit
from .config import AppConfig
import requests
import json
import pandas as pd
import numpy as np
import math
import pickle
from shapely.geometry import LineString

from PIL import Image
from io import BytesIO
import base64
# DEBUGGING
import sys
import os

api = Flask(__name__)
api.config.from_object(AppConfig)
api.secret_key = AppConfig.SECRET_KEY

# Set up CORS with specific origins and allow credentials
CORS(api, supports_credentials=True, origins=["http://localhost:3000"])
app_session = Session(api)
socket_io = SocketIO(api, cors_allowed_origins = "http://localhost:3000")

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

@api.route('/temperature/<int:year>', methods=['GET'])
def get_temperature_data(year):
    # Set parameters
    start = f"{year}-01-01"
    end = f"{year}-12-31"

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
        return jsonify({"error": "Failed to retrieve data"}), 500

    # Load JSON data
    try:
        newdata = json.loads(rawjson)['data']
    except json.JSONDecodeError as e:
        print('JSON Decode Error:', e)
        return jsonify({"error": "Failed to parse JSON"}), 500

    # Convert the JSON data into a dataframe
    final = pd.DataFrame()
    for entry in newdata:
        month_data = pd.DataFrame(entry[1], index=['avgt']).transpose()
        month_data.insert(0, 'month', entry[0])
        month_data = month_data.reset_index().rename(columns={'index': 'county'})
        month_data['year'] = year
        final = pd.concat([final, month_data])

    # Group by month and calculate average temperature
    monthly_avg = final.groupby('month').agg({'avgt': 'mean'}).reset_index()
    monthly_avg['year'] = year

    # Convert the aggregated data to a dictionary and return it
    temperature_data = monthly_avg.to_dict(orient='records')
    return jsonify(temperature_data)
    
@api.route('/precipitation/<int:year>', methods=['GET'])
def get_precipitation_data(year):
    start = f"{year}-01-01"
    end = f"{year}-12-31"
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
        return jsonify({"error": "HTTP error", "message": str(e)}), 500
    except requests.RequestException as e:
        return jsonify({"error": "Request failed", "message": str(e)}), 500
    except json.JSONDecodeError as e:
        return jsonify({"error": "Failed to parse JSON", "message": str(e)}), 500

    # Check if data is empty or not found
    if not rawjson.get('data'):
        return jsonify({"error": "No data found for specified parameters"}), 404

    # Process and return data
    final = pd.DataFrame()
    for entry in rawjson['data']:
        month_data = pd.DataFrame(entry[1], index=['pcpn']).transpose()
        month_data.insert(0, 'month', entry[0])
        month_data['year'] = year
        final = pd.concat([final, month_data])

    # Group by month and calculate average precipitation
    monthly_avg = final.groupby('month').agg({'pcpn': 'mean'}).reset_index()
    monthly_avg['year'] = year
    precipitation_data = monthly_avg.to_dict(orient='records')
    return jsonify(precipitation_data)

@api.route('/bird-data/<bird_name>')
@cross_origin(supports_credentials=True)
def get_bird_data(bird_name):
    if bird_name in DEMO_bird_data:
        return jsonify(DEMO_bird_data[bird_name])
    
@api.route('/prediction_input', methods=['POST'])
def predict():
    prediction_input = request.get_json()
    
    session['bird'] = prediction_input['bird']
    session['year'] = prediction_input['year']
    session['emissions'] = prediction_input['emissions']
        
    send_predictions()
    
    return "Processing Prediction"

def send_predictions():
    
    print(f"=== Info ===\nBird: {session['bird']}\nYear: {session['year']}\nEmissions: {session['emissions']}", file = sys.stderr)
    
    birdsModelDirs = {
        "warbler": "Setophaga_striata",
        "eagle": "Haliaeetus_leucocephalus",
        "anser": "Anser_albifrons",
        "curlew": "Numenius_americanus",
        "whimbrel": "Numenius_phaeopus"
    }
    
    # For image data:
    output_path = f"../model/outputs/png-images/{birdsModelDirs[session['bird']]}/{session['emissions']}/{session['year']}.png"
    dataImg = Image.open(output_path)
    buffer = BytesIO()
    dataImg.save(buffer, format="png")
    
    #If we'll need to encapsulate a file, use this:
    socket_io.emit("predictions", {
            "prediction": base64.b64encode(buffer.getvalue()).decode(),
            "resFormat": dataImg.format
    })

@api.route('/bird-info/<bird_name>')
def get_bird_info(bird_name):
    bird = DEMO_bird_data.get(bird_name)
    if bird:
        return jsonify({'name': bird_name, 'info': bird['info']})
    else:
        return jsonify({"error": "Invalid bird"}), 404

@api.route('/bird-sdm-data/<bird_name>')
def get_bird_sdm_data(bird_name):
    bird = DEMO_bird_data.get(bird_name)
    if bird:
        return jsonify({'name': bird_name, 'sdmData': bird['sdmData']})
    else:
        return jsonify({'error': 'Bird not found'}), 404

@api.route('/get_trajectory_data')
@cross_origin(supports_credentials=True)
def get_trajectory_data():
    selected_bird = request.args.get('bird')
    bird_id = request.args.get('birdID')
    filename = f'./data/{selected_bird}.csv'
    try:
        df = pd.read_csv(filename)
        df['ID'] = df['ID'].astype(str)
        # Filter data for the specified bird ID
        bird_data = df[df['ID'].str.contains(bird_id)]
        if bird_data.empty:
            return jsonify({'error': f'No trajectory data found for bird ID {bird_id}'})

        # Convert data to dictionary format
        trajectory_data = bird_data[['LATITUDE', 'LONGITUDE', 'TIMESTAMP']].to_dict(orient='records')
        return jsonify(trajectory_data)
    except FileNotFoundError:
        return jsonify({'error': f'CSV file for {selected_bird} not found'})

@api.route('/get_bird_ids')
@cross_origin(supports_credentials=True)
def get_bird_ids():
    selected_bird = request.args.get('bird')
    filename = f'./data/{selected_bird}.csv'
    try:
        df = pd.read_csv(filename)
        bird_ids = df['ID'].unique().tolist()
        return jsonify(bird_ids)
    except FileNotFoundError:
        return jsonify({'error': f'CSV file for {selected_bird} not found'})

@api.route('/get_general_migration')
@cross_origin(supports_credentials=True)
def get_general_migration():
    selected_bird = request.args.get('bird')
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
        
        
        return jsonify(segmented_polylines=simplified_polylines)
    
    except Exception as e:
        return jsonify(error=str(e)), 400
        
def simplify_line(coordinates, tolerance=0.1):
    line = LineString(coordinates)
    simplified_line = line.simplify(tolerance, preserve_topology=False)
    return list(zip(*simplified_line.xy))

@api.route('/get_heatmap_data')
@cross_origin(supports_credentials=True)
def get_heatmap_data():
    selected_bird = request.args.get('bird')
    filename = f'./app/data/{selected_bird}.csv'
    try:
        df = pd.read_csv(filename, low_memory=False)
        heatmap_data = df[['LATITUDE', 'LONGITUDE']].values.tolist()
        return jsonify(heatmap_data)
    except Exception as e:
        return jsonify(error=str(e)), 400    
    
if __name__ == '__main__':
    api.run(debug=True)
    socket_io.run(api, debug=True, port=5000)
