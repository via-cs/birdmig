from flask import Flask, jsonify, request, redirect, url_for, session
from flask_cors import CORS, cross_origin
# TEST for alpha.
from PIL import Image
from io import BytesIO
import base64
# Flask-React storing
from backend.config import AppConfig
from flask_session import Session

api = Flask(__name__)

# Configure the application from the AppConfig object.
api.config.from_object(AppConfig)
api.secret_key = AppConfig.SECRET_KEY

cors = CORS(api, supports_credentials = True)
app_session = Session(api)

# Test data.
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

@api.route('/bird-data/<bird_name>', methods = ['GET'])
@cross_origin(supports_credentials= True)
def get_bird_data(bird_name):
  
  # Trying to retreive data about the requested bird.
  # Save the requested bird for feeding the model.
  session['bird_name'] = bird_name
  
  # Using example data
  if bird_name in DEMO_bird_data:
    return jsonify(DEMO_bird_data[bird_name])
  else :
    print("Requested bird: [" + bird_name + "] is not cached.")
    return jsonify({"error": "Invalid bird"}), 404

# Running app
if __name__ == '__main__':
    api.run(debug=True)
    
@api.route('/bird-data/', methods = ['GET'])
@cross_origin(supports_credentials= True)
def get_model_output():
  # TODO: Read the model output.
  pass