from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

import queries_location


class ActionShowAccountNumber(Action):
    def name(self) -> Text:
        return "action_show_account_number"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        cnp = tracker.get_slot("cnp_slot")
        user = queries_location.find_user_by_cnp_query(cnp)

        if user:
            account_number = user["account_number"]
            dispatcher.utter_message(
                response="utter_show_account_number",
                account_number=account_number
            )
        else:
            dispatcher.utter_message("You are not logged in.")

        return [SlotSet("cnp_slot", None)]
