from typing import Text, List, Dict, Any
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

POTATO_INTENT = "potato_intent"


class ActionPotatoExample(Action):
    def name(self) -> Text:
        return "action_potato_example"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent_name = tracker.latest_message.get("intent").get("name")
        if intent_name == POTATO_INTENT:
            dispatcher.utter_message(response="utter_tomato")
        return []
