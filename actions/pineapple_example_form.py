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


class SubmitPineappleExampleForm(Action):
    def name(self) -> Text:
        return "submit_pineapple_example_form"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        return self.submit(dispatcher, tracker, domain)

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # Perform any custom actions here after form submission
        # For example, you can retrieve the values of the slots and save them to a database or file
        pineapple_slot_value = tracker.get_slot("pineapple_slot")
        if pineapple_slot_value == STOP:
            dispatcher.utter_message("Form has been stopped, no slots filled.")
            return [SlotSet("pineapple_slot", None)]
        dispatcher.utter_message("Submitted pineapple example form.")
        return [SlotSet("pineapple_slot", pineapple_slot_value)]
