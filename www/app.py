# Ref: https://github.com/bhavaniravi/rasa-site-bot
from flask import Flask
from flask import render_template,jsonify,request
import requests
# from models import *
#from engine import *
import random
import json


app = Flask(__name__)
app.secret_key = '12345'

@app.route('/')
def hello_world():
    return render_template('home.html')

get_random_response = lambda intent:random.choice(intent_response_dict[intent])


@app.route('/chat',methods=["POST"])
def chat():
    try:
        user_message = request.form["text"]
        
        # defining the api-endpoint
        API_ENDPOINT = "http://localhost:5004/chat/"

        # your API key here
        API_KEY = "XXXXXXXXXXXXXXXXX"

        # data to be sent to api
        data = { "sender": "default", "message": user_message}

        # sending post request and saving response as response object
        #response = requests.post(url = API_ENDPOINT, data = data)
        response = requests.post(API_ENDPOINT, json = data)

        response_text = response.json()
        print(response_text)
        return jsonify({"status":"success","response":response_text})
    except Exception as e:
        print(e)
        return jsonify({"status":"success","response":"Sorry I am not trained to do that yet..."})


app.config["DEBUG"] = True
if __name__ == "__main__":
    app.run(port=8090)
