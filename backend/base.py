
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
  
  bird_info = {
    "name": "No bird yet.",
    "about": "Try finding a bird to add",
    "output": bird_name
  }
  
  match bird_name:
    case "bird_1":
      
      dataImg = Image.open('DEBUG_Image.png')
      buffer = BytesIO()
      dataImg.save(buffer, format="png")
      
      bird_info = jsonify({
        "name": "bird_1",
        "about": "Generic info for bird 1",
        "output": base64.b64encode(buffer.getvalue()).decode(),
        "resFormat": dataImg.format
      })
    
  return bird_info
  
@api.route('/model_input', methods = ['POST'])
def choose_bird():
  requestJSON = request.get_json()
  requestJSON['data']
  
  return redirect(url_for('predict_bird'))