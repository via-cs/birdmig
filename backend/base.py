
from flask import Flask, render_template, request, session
from flask_cors import CORS, cross_origin
# Libraries to help with ML
import pandas
import numpy as np

api = Flask(__name__)
cors = CORS(api)
api.config['CORS_HEADERS'] = 'Content-Type'
api.secret_key = 'outset'

#session['req'] = "None"


@api.route('/profile', methods = ['GET'])
def my_profile():
    
    currentRequest = session['req'] if 'req' in session else "None"
    if(currentRequest == "None") :
      return {
        "name": "",
        "about": "",
        "output": "Click on an option to obtain data!"}
    
    response_body = {
        "name": "Bird Mig",
        "about": "ALPHA: Waiting for model to complete",
        "output": "dumb"
    }

    return response_body
  
@api.route('/choose_bird', methods = ['POST'])
def choose_bird():
  requestJSON = request.get_json()
  return {
        "name": "Bird Mig",
        "about": "ALPHA: Waiting for model to complete",
        "output": "dumb"
    }