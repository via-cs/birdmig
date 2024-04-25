import os
from flask import Flask, jsonify, render_template, request, session
from flask_cors import CORS, cross_origin
from jinja2 import TemplateNotFound
# TEST for alpha.
#from PIL import Image
#from io import BytesIO
#import base64
# Flask-React storing
from flask_session import Session
from .config import AppConfig
# debug
import sys


api = Flask(__name__)

# Configure the application from the AppConfig object.
api.config.from_object(AppConfig)
api.secret_key = AppConfig.SECRET_KEY

cors = CORS(api, supports_credentials = True)
app_session = Session(api)

# Example data for demonstration purposes.
DEMO_bird_data = {
    "Bird 1": {
        "info": "Blackpoll Warbler",
        "sdmData": [{"x": 1, "y": 300}, {"x": 2, "y": 600}, {"x": 3, "y": 800}],
    },
    "Bird 2": {
        "info": "Bald Eagle",
        "sdmData": [{"x": 1, "y": 100}, {"x": 2, "y": 200}, {"x": 3, "y": 500}],
    },
    "Bird 3": {
        "info": "White Fronted Goose",
        "sdmData": [{"x": 1, "y": 300}, {"x": 2, "y": 600}, {"x": 3, "y": 800}],
    },
    "Bird 4": {
        "info": "Long Billed Curlew",
        "sdmData": [{"x": 1, "y": 300}, {"x": 2, "y": 600}, {"x": 3, "y": 800}],
    },
    "Bird 5": {
        "info": "Whimbrel",
        "sdmData": [{"x": 1, "y": 300}, {"x": 2, "y": 600}, {"x": 3, "y": 800}],
    },
}

@api.route('/prediction_input', methods= ['POST'])
@cross_origin(supports_credentials= True)
def SendClimateVars():
  sent_details = request.get_json()
  
  session['year'] = sent_details['year']
  session['emissions'] = sent_details['emissions']
  
  return "Received predictor variables successfully"


@api.route('/bird-data/<bird_name>', methods = ['POST'])
@cross_origin(supports_credentials= True)
def get_bird_data(bird_name):
  
  # Trying to retreive data about the requested bird.
  # Save the requested bird for feeding the model.
  session['bird_name'] = bird_name
  
  print("Session contents: " + str(len(session)), file=sys.stderr)
  
  # Using example data
  if bird_name in DEMO_bird_data:
    return jsonify(DEMO_bird_data[bird_name])
  else :
    return jsonify({"error": "Invalid bird"}), 404

@api.route('/bird-info/<bird_name>')
def get_bird_info(bird_name):
    """Endpoint to retrieve only bird information."""
    bird = DEMO_bird_data.get(bird_name)
    if bird:
        return jsonify({'name': bird_name, 'info': bird['info']})
    else:
        return jsonify({'error': 'Bird not found'}), 404

@api.route('/bird-sdm-data/<bird_name>')
def get_bird_sdm_data(bird_name):
    """Endpoint to retrieve only bird SDM data."""
    bird = DEMO_bird_data.get(bird_name)
    if bird:
        return jsonify({'name': bird_name, 'sdmData': bird['sdmData']})
    else:
        return jsonify({'error': 'Bird not found'}), 404
    
@api.route('/migration_images/<filename>')
def migration_image(filename):
    """Endpoint to render a specific migration image."""
    try:
        if not filename.endswith('.html'):
            filename += '.html'
        return render_template(filename)
    except TemplateNotFound as e:
        return f'Template not found: {e}', 404

# Running app
if __name__ == '__main__':
    api.run(debug=True)