from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet
import requests

class ActionExchange(Action):
	def name(self):
		return 'action_exchange'
		
	def run(self, dispatcher, tracker, domain):
		
		# Set the api api_key
		api_key = 'use your api key'
		
		currency = tracker.get_slot('currency')

		params = {'access_key': api_key, 'currencies': currency, 'format': 1}
		response = requests.get('http://apilayer.net/api/live', params = params)

		# Error handling

		# Check for HTTP codes other than 200
		if response.status_code != 200:
    			print('Status:', response.status_code, 'Problem with the request. Exiting.')
    			exit()

		exchrates = response.json()

		#print(exchrates['quotes']['USDINR'])

		#print(exchrates['quotes']['USD'+currency])
		exchangerate = exchrates['quotes']['USD'+str(currency).upper()]

		response = """ The exchange rate of {} for today is {} against 1 USD. """.format(currency,exchangerate) 
						
		dispatcher.utter_message(response)
		return [SlotSet('currency',currency)]

