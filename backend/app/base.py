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
