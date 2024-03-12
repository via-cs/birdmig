
from flask import Flask, jsonify, request, redirect, url_for
from flask_cors import CORS, cross_origin
# TEST for alpha.
from PIL import Image
from io import BytesIO
import base64

api = Flask(__name__)
cors = CORS(api)
api.config['CORS_HEADERS'] = 'Content-Type'


@api.route('/profile', methods = ['GET'])
def predict_bird():
      
    return generate_output("bird_1")
  
def generate_output(bird_name):
  
  bird_info = "Try finding a bird to add."
  
  match bird_name:
    case "bird_1":
    
      data_url = 'DEBUG_Image.png'
      bird_info = "Generic info for unique bird 1",

    case "bird_2":
      
      data_url = 'ALPHA_DemoMap.png'
      bird_info = "Generic info for different bird 2",    
  
  # TODO: replace the content for the image data with the actual
  # ML output.
  dataImg = Image.open(data_url)
  buffer = BytesIO()
  dataImg.save(buffer, format="png")
  
  return jsonify({
    "name": bird_name,
    "about": bird_info,
    "output": base64.b64encode(buffer.getvalue()).decode(),
    "resFormat": dataImg.format
  })
  
@api.route('/model_input', methods = ['POST'])
def choose_bird():
  requestJSON = request.get_json()
  requestJSON['data']
  
  return generate_output(requestJSON['data'])#redirect(url_for('predict_bird'))