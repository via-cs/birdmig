from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

api = Flask(__name__)
cors = CORS(api)
api.config['CORS_HEADERS'] = 'Content-Type'

bird_data_example = {
    "Bird 1": {
        "info": "Information about Bird 1",
        "sdmData": [{"x": 1, "y": 300}, {"x": 2, "y": 600}, {"x": 3, "y": 800}],
        "timeSeriesData": {
            "precipitation": [100, 200, 300],
            "climate": [20, 21, 22],
            "temperature": [30, 32, 33],
        },
    },
    "Bird 2": {
        "info": "Information about Bird 2",
        "sdmData": [{"x": 1, "y": 100}, {"x": 2, "y": 200}, {"x": 3, "y": 500}],
        "timeSeriesData": {
            "precipitation": [300, 400, 500],
            "climate": [30, 40, 50],
            "temperature": [60, 70, 80],
        },
    }
    # Add more dummy data for other birds as needed
}

@api.route('/bird-data/<bird_name>')
@cross_origin()
def get_bird_data(bird_name):
    # using example data
    bird_info = bird_data_example.get(bird_name)
    if bird_info:
        return jsonify(bird_info)
    else:
        return jsonify({"error": "Bird not found"}), 404

# Running app
if __name__ == '__main__':
    api.run(debug=True)