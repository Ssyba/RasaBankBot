from typing import Any, Dict, List, Text
from rasa_sdk import Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import queries_location
from actions.base_classes import BaseFormValidationAction, BaseSubmitAction


class ValidateFeedbackForm(BaseFormValidationAction):
    def name(self) -> Text:
        return "validate_feedback_form"

    async def validate_feedback_slot(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        if len(slot_value) < 1:
            dispatcher.utter_message(
                text="Please provide a feedback of at least 1 character.")
            return {"feedback_slot": None}
        else:
            return {"feedback_slot": slot_value}


class ActionSubmitFeedbackForm(BaseSubmitAction):
    def name(self) -> Text:
        return "submit_feedback_form"

    async def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        cnp = tracker.get_slot("cnp_slot")
        feedback = tracker.get_slot("feedback_slot")

        queries_location.insert_feedback_query(cnp, feedback)

        dispatcher.utter_message(text="Feedback received. Thank you!")
        return [
            SlotSet('cnp_slot', cnp),
            SlotSet('logged_in_status_slot', True),
            SlotSet('feedback_slot', None)
        ]
