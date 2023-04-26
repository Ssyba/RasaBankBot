from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from general_methods import only_works_if_logged_out


# Created as a way to help in development
class ActionLogMeIn(Action):

    def name(self) -> Text:
        return "action_log_me_in"

    @only_works_if_logged_out
    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="You are logged in.")
        return [SlotSet('cnp_slot', "0001"),
                SlotSet('logged_in_status_slot', True),
                ]
