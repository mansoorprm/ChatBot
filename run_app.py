from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 25 22:47:24 2018

@author: mansoorparambath
"""
"""
https://github.com/RasaHQ/rasa_core/issues/119
"""



import logging

from rasa_core.channels import HttpInputChannel
from rasa_core import utils
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.channels.channel import UserMessage
from rasa_core.channels.direct import CollectingOutputChannel
from rasa_core.channels.rest import HttpInputComponent
from flask import Blueprint, request, jsonify
import json


logger = logging.getLogger(__name__)
class SimpleWebBot(HttpInputComponent):
    """A simple web bot that listens on a url and responds."""

    def blueprint(self, on_new_message):
        custom_webhook = Blueprint('custom_webhook', __name__)

        @custom_webhook.route("/status", methods=['GET'])
        def health():
            return jsonify({"status": "ok"})

        @custom_webhook.route("/", methods=['POST'])
        def receive():
            payload = json.loads(str(request.data,"utf-8"))
            print(payload)
            print("responses")
            sender_id = payload.get("sender", None)
            text = payload.get("message", None)
	    #sender_id = payload.get("sender", None)
            #text = payload.get("message", None)
            out = CollectingOutputChannel()
            on_new_message(UserMessage(text, out, sender_id))
            #responses = [m for _, m in out.messages]
            responses = [m["text"] for m in out.messages]
            print(str(responses).strip('[]').replace('},', '}'))
            return json.dumps(str(responses).strip('[]').replace('},', '}'))

        return custom_webhook

def run(serve_forever=True):
    #path to your NLU model
    interpreter = RasaNLUInterpreter("./models/nlu/default/exchangenlu")
    # path to your dialogues models
    agent = Agent.load("models/dialogue", interpreter=interpreter)
    #http api endpoint for responses
    input_channel = SimpleWebBot()
    if serve_forever:
        agent.handle_channel(HttpInputChannel(5004, "/chat", input_channel))
    return agent

if __name__ == "__main__":
    utils.configure_colored_logging(loglevel="INFO")
    run()
