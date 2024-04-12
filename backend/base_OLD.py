from flask import Flask, jsonify, request, redirect, url_for, session
from flask_cors import CORS, cross_origin
# Imports for image/data processing.
from PIL import Image
from io import BytesIO
import base64
# Flask-React storing
from config import AppConfig
from flask_session import Session

api = Flask(__name__)

# Configure the application from the AppConfig object.
api.config.from_object(AppConfig)
api.secret_key = AppConfig.SECRET_KEY

cors = CORS(api, supports_credentials = True)
app_session = Session(api)

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

#debug
import sys

@api.route('/model-input/<bird_name>', methods = ['POST'])
@cross_origin(supports_credentials= True)
def request_bird(bird_name):

  # Try to save the session data.
  print("elements in session: " + str(len(session)), file=sys.stderr)
  session['bird_name'] = bird_name
  
  debug_msg = "session has: ["
  for item in session:
    debug_msg = debug_msg + item + ", "
  print(debug_msg + "] as part of its saved session variables", file=sys.stderr)
  
  # Return some dummy data.
  return jsonify({
    "msg": "now click \"get bird\" to see info about the bird you want."})
  

@api.route('/model-output', methods = ['GET'])
@cross_origin(supports_credentials= True)
def get_cached_bird_data():
  
  print("Elements in session: " + str(len(session)), file=sys.stderr)
  requested_bird = session.get('bird_name')
  
  # Using example data
  if (requested_bird) and (requested_bird in DEMO_bird_data):
    print("The requested bird was " + requested_bird, file=sys.stderr)
    
    return jsonify({
      "msg": "The bird that was previously requested was: [" + requested_bird + "]"
    })
  elif(requested_bird):
    print("Requested bird: [" + requested_bird + "] is not a cached bird", file=sys.stderr)
    
    return jsonify({"error": "Invalid bird"}), 404
  else:
    print("Expected a bird, but got nothing from session.", file=sys.stderr)
    
    return jsonify({"error": "Invalid bird"}), 404

# Running app
if __name__ == '__main__':
    api.run(debug=True)