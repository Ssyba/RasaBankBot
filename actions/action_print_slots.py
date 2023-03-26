from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionPrintSlots(Action):

    def name(self) -> Text:
        return "action_print_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        slots = tracker.slots
        dispatcher.utter_message(str(slots))
        return []
