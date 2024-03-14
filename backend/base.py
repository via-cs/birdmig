from flask import Flask, jsonify, request, redirect, url_for, session
from flask_cors import CORS, cross_origin
from flask_session import Session, sessions
# TEST for alpha.
from PIL import Image
from io import BytesIO
import base64

api = Flask(__name__)
cors = CORS(api)
api.config['CORS_HEADERS'] = 'Content-Type'

# Session enabling
api.secret_key = "burd"

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

@api.route('/model-input', methods = ['POST'])
@cross_origin
def request_bird(bird_name):
  print("elements in session: " + str(len(session)))
  session['requested_bird'] = bird_name
  
  for item in session:
    print("session has: [" + item + "] as part of its saved session variables")
  return jsonify({"msg": "now click \"get bird\" to see info about the bird you want."})
  

@api.route('/model-output', methods = ['GET'])
@cross_origin()
def get_cached_bird_data():
  
  requested_bird = session.get('requested_bird')
  
  # Using example data
  if (requested_bird) and (requested_bird in DEMO_bird_data):
    return jsonify({
      "msg": "The bird that was previously requested was: [" + requested_bird + "]"
    })
  else :
    print("Requested bird: [" + requested_bird + "] is not a valid bird :/")
    return jsonify({"error": "Invalid bird"}), 404

# Running app
if __name__ == '__main__':
    api.run(debug=True)