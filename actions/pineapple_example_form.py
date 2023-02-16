from typing import Dict, Any, Text, List

from rasa_sdk import FormValidationAction, Tracker, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import SlotSet

STOP = "stop"


class ValidatePineappleExampleForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_pineapple_example_form"

    def validate_pineapple_slot(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        user_input = slot_value.lower()
        if user_input in ["fill", "stop"]:
            return {"pineapple_slot": user_input}
        else:
            return {"pineapple_slot": None}
