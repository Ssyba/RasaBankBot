from typing import Dict, Any, Text, List
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import SlotSet
import queries_location
import logging
from actions.base_classes import BaseFormValidationAction, BaseSubmitAction
from general_methods import is_valid_cnp, is_valid_password, message_for_logged_in, skip_validate_if_logged_in, \
    handle_break_and_logout_special_intents

logger = logging.getLogger(__name__)


class ValidateLoginForm(BaseFormValidationAction):
    def name(self) -> Text:
        return "validate_login_form"

    @skip_validate_if_logged_in
    @handle_break_and_logout_special_intents
    async def validate_cnp_slot(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if not is_valid_cnp(slot_value):
            dispatcher.utter_message(template="utter_invalid_cnp")
            return {"cnp_slot": None}

        cnp = slot_value
        user = queries_location.find_user_by_cnp_query(cnp)

        # If the user is not in the DB, the password slot is skipped and the user is informed
        if user:
            return {"cnp_slot": cnp}
        else:
            return {"password_slot": "skipped"}

    async def validate_password_slot(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        cnp = tracker.get_slot("cnp_slot")
        user = queries_location.find_user_by_cnp_query(cnp)
        if is_valid_password(slot_value) and slot_value == user['password']:
            return {"requested_slot": None}  # This finishes to validate for all slots and moves to submit
        dispatcher.utter_message(template="utter_wrong_password")
        return {"password_slot": None}


class SubmitLoginForm(BaseSubmitAction):
    def name(self) -> Text:
        return "submit_login_form"

    @message_for_logged_in
    async def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        logged_in_status = tracker.get_slot('logged_in_status_slot')
        if logged_in_status:
            dispatcher.utter_message(
                text="You are already logged in.")
            return []

        if tracker.get_slot("password_slot") == "skipped":
            dispatcher.utter_message(template="utter_user_not_found")
            buttons = [
                {"payload": "/check_cnp_again_intent", "title": "I am an existing user, I want to check my CNP again."},
                {"payload": "/new_user_intent", "title": "I am a new user and I wish to create an account."},
                {"payload": "/leave_app_intent", "title": "I wish to leave the app."},
                {"payload": "/policies_info_intent", "title": "Give me information about your policies."}
            ]

            dispatcher.utter_button_message(
                "Please choose one of the following options:",
                buttons=buttons
            )
            return [SlotSet("cnp_slot", None), SlotSet("password_slot", None)]

        cnp = tracker.get_slot("cnp_slot")
        user = queries_location.find_user_by_cnp_query(cnp)

        dispatcher.utter_message(f"Welcome {user['surname']}, how can I help you today?")

        return [SlotSet("cnp_slot", cnp), SlotSet("password_slot", None), SlotSet("logged_in_status_slot", True)]
