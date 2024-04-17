import os
from flask import Flask, jsonify, render_template
from flask_cors import CORS, cross_origin
from jinja2 import TemplateNotFound

# Importing for potential image manipulation, not used directly in provided code.
from PIL import Image
from io import BytesIO
import base64

api = Flask(__name__, template_folder='../templates')
CORS(api)
api.config['CORS_HEADERS'] = 'Content-Type'

# Example data for demonstration purposes.
DEMO_bird_data = {
    "Bird 1": {
        "info": "Generic info for unique bird 1",
        "sdmData": [{"x": 1, "y": 300}, {"x": 2, "y": 600}, {"x": 3, "y": 800}],
    },
    "Bird 2": {
        "info": "Generic info for different bird 2",
        "sdmData": [{"x": 1, "y": 100}, {"x": 2, "y": 200}, {"x": 3, "y": 500}],
    },
    "Bird 3": {
        "info": "Generic info for unique bird 3",
        "sdmData": [{"x": 1, "y": 300}, {"x": 2, "y": 600}, {"x": 3, "y": 800}],
    },
    "Bird 4": {
        "info": "Generic info for unique bird 4",
        "sdmData": [{"x": 1, "y": 300}, {"x": 2, "y": 600}, {"x": 3, "y": 800}],
    },
    "Bird 5": {
        "info": "Generic info for unique bird 5",
        "sdmData": [{"x": 1, "y": 300}, {"x": 2, "y": 600}, {"x": 3, "y": 800}],
    },
}

@api.route('/bird-data/<bird_name>')
@cross_origin()
def get_bird_data(bird_name):
    if bird_name in DEMO_bird_data:
        return jsonify(DEMO_bird_data[bird_name])
    else:
        print(f"Requested bird: [{bird_name}] is not cached.")
        return jsonify({"error": "Invalid bird"}), 404
  
@api.route('/migration_images/<filename>')
def migration_image(filename):
    print(f"Attempting to render: {filename}")
    try:
        if not filename.endswith('.html'):
            filename += '.html'
        return render_template(filename)
    except TemplateNotFound as e:
        print(f"Error: {e}")
        return 'Template not found', 404


# Running app
if __name__ == '__main__':
    api.run(debug=True)
