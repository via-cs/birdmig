from flask import Flask, jsonify, request, session, send_from_directory
from flask_cors import CORS
from flask_session import Session
from .config import AppConfig

api = Flask(__name__)
api.config.from_object(AppConfig)
api.secret_key = AppConfig.SECRET_KEY

cors = CORS(api, supports_credentials=True)
app_session = Session(api)

DEMO_bird_data = {
    "Blackpoll Warbler": {
        "info": "Migration details about Blackpoll Warbler",
        "sdmData": [{"x": 1, "y": 300}, {"x": 2, "y": 600}, {"x": 3, "y": 800}],
    },
    "Bald Eagle": {
        "info": "Migration details about Bald Eagle",
        "sdmData": [{"x": 1, "y": 100}, {"x": 2, "y": 200}, {"x": 3, "y": 500}],
    },
    "White Fronted Goose": {
        "info": "Migration details about White Fronted Goose",
        "sdmData": [{"x": 1, "y": 300}, {"x": 2, "y": 600}, {"x": 3, "y": 800}],
    },
    "Long Billed Curlew": {
        "info": "Migration details about Long Billed Curlew",
        "sdmData": [{"x": 1, "y": 300}, {"x": 2, "y": 600}, {"x": 3, "y": 800}],
    },
    "Whimbrel": {
        "info": "Migration details about Whimbrel",
        "sdmData": [{"x": 1, "y": 300}, {"x": 2, "y": 600}, {"x": 3, "y": 800}],
    },
}

@api.route('/prediction_input', methods=['POST'])
def send_climate_vars():
    sent_details = request.get_json()
    session['year'] = sent_details['year']
    session['emissions'] = sent_details['emissions']
    return "Received predictor variables successfully"

@api.route('/bird-info/<bird_name>')
def get_bird_info(bird_name):
    bird = DEMO_bird_data.get(bird_name)
    if bird:
        return jsonify({'name': bird_name, 'info': bird['info']})
    else:
        return jsonify({'error': 'Bird not found'}), 404

@api.route('/bird-sdm-data/<bird_name>')
def get_bird_sdm_data(bird_name):
    bird = DEMO_bird_data.get(bird_name)
    if bird:
        return jsonify({'name': bird_name, 'sdmData': bird['sdmData']})
    else:
        return jsonify({'error': 'Bird not found'}), 404
    
@api.route('/json/<filename>')
def send_json(filename):
    return send_from_directory('climate_data/json_data', filename)

if __name__ == '__main__':
    api.run(debug=True)
