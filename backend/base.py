
from flask import Flask, jsonify, request, redirect, url_for
from flask_cors import CORS, cross_origin
# TEST for alpha.
from PIL import Image
from io import BytesIO
import base64

api = Flask(__name__)
cors = CORS(api)
api.config['CORS_HEADERS'] = 'Content-Type'

@api.route('/bird-data/<bird_name>')
# @api.route('/model_input', methods = ['POST'])
@cross_origin()
def get_bird_data(bird_name):
  
  #requestJSON = request.get_json()
  #requestJSON['data']
  
  return generate_output(bird_name)
  
  # using example data
  # bird_info = bird_data_example.get(bird_name)
  #return generate_output(bird_name)
  #if bird_info:
  #    return jsonify(bird_info)
  #else:
  #    return jsonify({"error": "Bird not found"}), 404

# Running app
if __name__ == '__main__':
    api.run(debug=True)
  
def generate_output(bird_name):
  
  bird_info = "Try finding a bird to add."
  
  match bird_name:
    case "None":
      return jsonify({"error": "Bird not founnd"}), 404
    case "bird_1":
    
      #data_url = 'DEBUG_Image.png',
      sdm_dat = [{"x": 1, "y": 300}, {"x": 2, "y": 600}, {"x": 3, "y": 800}],
      time_series = {
            "precipitation": [100, 200, 300],
            "climate": [20, 21, 22],
            "temperature": [30, 32, 33],
      }
      bird_info = "Generic info for unique bird 1",

    case "bird_2":
      
      #data_url = 'ALPHA_DemoMap.png'
      bird_info = "Generic info for different bird 2"
      sdm_dat = [{"x": 1, "y": 100}, {"x": 2, "y": 200}, {"x": 3, "y": 500}]
      time_series = {
            "precipitation": [300, 400, 500],
            "climate": [30, 40, 50],
            "temperature": [60, 70, 80],
      } 
        
  
  # TODO: replace the content for the image data with the actual
  # ML output.
  # For now, this doesn't do anything, but we may need it for sending
  # base64 encodings for ML output.
  
  #dataImg = Image.open(data_url)
  #buffer = BytesIO()
  #dataImg.save(buffer, format="png")
  
  return jsonify({
    {
        "info": bird_info,
        "sdmData": sdm_dat,
        "timeSeriesData": time_series,
        #"prediction": base64.b64encode(buffer.getvalue()).decode(),
        #"resFormat": dataImg.format
    }
  })
