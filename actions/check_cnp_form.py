from typing import Dict, Any, Text, List
from rasa_sdk import FormValidationAction, Tracker, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import SlotSet
from queries_location import find_user_name_by_cnp_query
from helper_methods import find_in_db
import logging

logger = logging.getLogger(__name__)


class ValidateCheckCNPForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_check_cnp_form"

    def validate_cnp_slot(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if len(slot_value) != 4:
            dispatcher.utter_message("CNP should be 4 digits long.")
            return {"cnp_slot": None}
        try:
            int(slot_value)
            return {"cnp_slot": slot_value}
        except ValueError:
            dispatcher.utter_message("Each CNP character should be a digit.")
            return {"cnp_slot": None}


class SubmitCheckCNPForm(Action):
    def name(self) -> Text:
        return "submit_check_cnp_form"

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
        cnp = tracker.get_slot("cnp_slot")
        name_query = find_user_name_by_cnp_query(cnp)
        name = find_in_db(name_query)
        if name:
            dispatcher.utter_message(f"Welcome {name[0][0]}, how can I help you today?")
        else:
            dispatcher.utter_message("No user found.")

        return [SlotSet("cnp_slot", None)]
