from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import ActiveLoop
import queries_location


class ActionShowBalance(Action):
    def name(self) -> Text:
        return "action_show_balance"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        cnp_slot = tracker.get_slot('cnp_slot')

        if cnp_slot is not None:
            balance = queries_location.get_balance_by_cnp(cnp_slot)
            message = f"Your current balance is ${balance}. You have been logged out."
        else:
            message = "You are not logged in."

        dispatcher.utter_message(text=message)
        return [ActiveLoop(None)]
