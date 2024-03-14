from flask import Flask, jsonify, request, redirect, url_for
from flask_cors import CORS, cross_origin
# TEST for alpha.
from PIL import Image
from io import BytesIO
import base64

api = Flask(__name__)
cors = CORS(api)
api.config['CORS_HEADERS'] = 'Content-Type'

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
  
  # Using example data
  if bird_name in DEMO_bird_data:
    return jsonify(DEMO_bird_data[bird_name])
  else :
    print("Requested bird: [" + bird_name + "] is not cached.")
    return jsonify({"error": "Invalid bird"}), 404

# Running app
if __name__ == '__main__':
    api.run(debug=True)