from flask import Flask, jsonify, request, session, send_from_directory
from flask_cors import CORS, cross_origin
from flask_session import Session
from flask_socketio import SocketIO, emit
from .config import AppConfig
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

api = Flask(__name__)
api.config.from_object(AppConfig)
api.secret_key = AppConfig.SECRET_KEY

with open('./models/svm_classifier_model.pkl', 'rb') as f:
    model = pickle.load(f)

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

@api.route('/bird-data/<bird_name>')
@cross_origin(supports_credentials=True)
def get_bird_data(bird_name):
    if bird_name in DEMO_bird_data:
        return jsonify(DEMO_bird_data[bird_name])
    
@api.route('/prediction_input', methods=['POST'])
def predict():
    prediction_input = request.get_json()

    session['year'] = prediction_input['year']
    session['emissions'] = prediction_input['emissions']
        
    send_predictions()
    
    return "Processing Prediction"#jsonify({'prediction': send_predictions()})

#@socket_io.on("predict")
def send_predictions():
    print("Predicting something....", file = sys.stderr)
    
    # prediction_df = pd.read_csv('./data/warbler.csv')
    # Dummy data genereated to quickly debug the predictions.
    prediction_df = pd.DataFrame({f"X{i}": range(25 * i, 25 * (i + 1)) for i in range(19)})
    
    prediction_result = model.predict(prediction_df)
    
    print(prediction_result, file = sys.stderr)
    
    '''
    # For image data:
    dataImg = Image.open(<insert URL for the image here>)
    buffer = BytesIO()
    dataImg.save(buffer, format="png")
    
    #If we'll need to encapsulate a file, use this:
    socket_io.emit("predictions", {
            "prediction": base64.b64encode(buffer.getvalue()).decode(),
            "resFormat": dataImg.format
    })
    
    # The front end (App.js) will also need changes to properly display the sent image, displaying the prediction base64 array as the image format specified in the resFormat field.
    # A google search may be necessary for having react.js display a base64 array(?) of data as a specified image format.
    '''
    
    socket_io.emit("predictions", {'prediction': "prediction_result.tolist()"})
    

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
    
@api.route('/json/<filename>')
def send_json(filename):
    return send_from_directory('climate_data/json_data', filename)

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

if __name__ == '__main__':
    api.run(debug=True)
    socket_io.run(api, debug=True, port=5000)
