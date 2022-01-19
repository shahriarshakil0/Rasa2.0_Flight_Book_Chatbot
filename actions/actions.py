# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.events import Restarted
from rasa_sdk.events import SlotSet
from .api_flight import get_flight




class ActionHotel(Action):
    '''Book Flight'''
    def name(self) -> Text:
        return "action_flight"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            dep_city = tracker.get_slot("dep_city")
            arr_city = tracker.get_slot("arr_city")
            dep_date = tracker.get_slot("dep_date")
            data = get_flight(dep_city,arr_city,dep_date)
            # print(type(data))
            # print(data[0])
            # print(data[1])
            # print(data[2])

            # print("**********")
            # for i in data[2]:
            #     print(type(i))
            for i in data[2]['airport']:
                # print(i)
                if i['code'] == data[0]:
                    # print(i['code'])
                    departure_airport = i['name']
                    departure_city = i['city']
                    departure_country = i['country']
                    departure_location = f"Your departure location is '{departure_airport}, {departure_city},{departure_country}'."
                    # print(departure_location)

            for i in data[2]['airport']:
                # print(i)
                if i['code'] == data[1]:
                    # print(i['code'])
                    arrival_airport = i['name']
                    arrival_city = i['city']
                    arrival_country = i['country']
                    arrival_location = f"Your arrival location is '{arrival_airport}, {arrival_city},{arrival_country}'."
                    # print(arrival_location)
                    # print("\n")

            response1 = f"{departure_location}\n{arrival_location}\nHere, some flight information -\n"
            # dispatcher.utter_message("\n")
            dispatcher.utter_message(response1)
            flight_info = data[2]['airline']
            for i in flight_info[0:5]:
                try:
                    name = i['name']
                except:
                    name = "Not available"
                try:
                    book = i['checkInUrl']
                except:
                    book = "Not available"
                try:
                    phone_number = i['phoneNumber']
                    website = i['websiteUrl']
                except:
                    phone_number = "Not available"
                    website = "Not available"
                
                
                response2 = f"Airline name- '{name}';\nFor booking- '{book}';\nAny information- '{phone_number}', '{website}'\n"
                # print(response2)
                # dispatcher.utter_message("\n")
                dispatcher.utter_message(response2)

        except:
            dispatcher.utter_message("Please give me right information.")

        return [SlotSet('dep_city',dep_city),SlotSet('arr_city',arr_city),SlotSet('dep_date',dep_date)]


class ActionClear(Action):
    '''Reset All'''
    def name(self) -> Text:
        return "action_clear"

    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return [AllSlotsReset()]

