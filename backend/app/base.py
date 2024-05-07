from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import pandas as pd
import numpy as np
import math
from shapely.geometry import LineString

api = Flask(__name__)
cors = CORS(api)
api.config['CORS_HEADERS'] = 'Content-Type'

# Example bird data dictionary
DEMO_bird_data = {
    "Bird 1": {
        "info": "Generic info for unique bird 1",
        "sdmData": [{"x": 1, "y": 300}, {"x": 2, "y": 600}, {"x": 3, "y": 800}],
        "timeSeriesData": {
            "precipitation": [300, 400, 500],
            "climate": [30, 40, 50],
            "temperature": [60, 70, 80],
        },
    },
    "Bird 2": {
        "info": "Generic info for different bird 2",
        "sdmData": [{"x": 1, "y": 100}, {"x": 2, "y": 200}, {"x": 3, "y": 500}],
        "timeSeriesData": {
            "precipitation": [300, 400, 500],
            "climate": [30, 40, 50],
            "temperature": [60, 70, 80],
        }
    }
}

@api.route('/bird-data/<bird_name>')
@cross_origin()
def get_bird_data(bird_name):
    if bird_name in DEMO_bird_data:
        return jsonify(DEMO_bird_data[bird_name])
    else:
        return jsonify({"error": "Invalid bird"}), 404

@api.route('/get_trajectory_data')
@cross_origin()
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
@cross_origin()
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
@cross_origin()
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
@cross_origin()
def get_kde_data():
    selected_bird = request.args.get('bird')
    filename = f'./data/{selected_bird}.csv'
    
    try:
        df = pd.read_csv(filename, low_memory=False)
        heatmap_data = df[['LATITUDE', 'LONGITUDE']].values.tolist()
        return jsonify(heatmap_data)
    except Exception as e:
        return jsonify(error=str(e)), 400    
    
if __name__ == '__main__':
    api.run(debug=True)
