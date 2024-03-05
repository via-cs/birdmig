
from flask import Flask
from flask_cors import CORS, cross_origin

api = Flask(__name__)
cors = CORS(api)
api.config['CORS_HEADERS'] = 'Content-Type'


@api.route('/profile')
def my_profile():
    response_body = {
        "name": "BirdMig",
        "about" :"ALPHA_DEMONSTRATION"
    }

    return response_body
    
# Running app
if __name__ == '__main__':
    api.run(debug=True)