from flask import Flask

api = Flask(__name__)

@api.route('/profile')
def my_profile():
    response_body = {
        "name": "BirdMig",
        "about" :"Hello from ECS193A Group 22!"
    }

    return response_body