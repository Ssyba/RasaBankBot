from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset, ActiveLoop


class ActionLogout(Action):
    def name(self) -> Text:
        return "action_logout"

    async def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("You have been logged out.")
        return [AllSlotsReset(), ActiveLoop(None)]
