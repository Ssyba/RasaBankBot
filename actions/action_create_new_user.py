from typing import Dict, Any, Text, List
from rasa_sdk import FormValidationAction, Tracker, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import SlotSet
import logging
import queries_location

logger = logging.getLogger(__name__)


class ValidateNewUserForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_new_user_form"

    def validate_cnp_slot(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        cnp = slot_value

        if not (len(cnp) == 4 and cnp.isdigit()):
            dispatcher.utter_message("CNP should be 4 digits long, and each character should be a digit.")
            return {"cnp_slot": None}

        user = queries_location.find_user_by_cnp_query(cnp)

        if user:
            return {"cnp_slot": cnp, "requested_slot": None}
        else:
            return {"cnp_slot": cnp}

    def validate_name_slot(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        if not (slot_value.isalpha() and 4 <= len(slot_value) <= 35):
            dispatcher.utter_message(
                "Name should be at least 4 characters long, have a maximum of 35 characters, and only contain letters.")
            return {"name_slot": None}
        else:
            return {"name_slot": slot_value}

    def validate_surname_slot(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        if not (slot_value.isalpha() and 4 <= len(slot_value) <= 35):
            dispatcher.utter_message(
                "Surname should be at least 4 characters long, have a maximum of 35 characters, and only contain "
                "letters.")
            return {"surname_slot": None}
        return {"surname_slot": slot_value}

    def validate_age_slot(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        try:
            age = int(slot_value)
            if age <= 0:
                dispatcher.utter_message("Age should be a positive number.")
                return {"age_slot": None}
            elif age < 18:
                dispatcher.utter_message("You must be at least 18 years old to register.")
                return {"age_slot": None}
            else:
                return {"age_slot": age}
        except ValueError:
            dispatcher.utter_message("Age should be a number and under 99.")
            return {"age_slot": None}

    def validate_password_slot(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if len(slot_value) < 8:
            dispatcher.utter_message("Password should be at least 8 characters long.")
            return {"password_slot": None}
        return {"password_slot": slot_value}

    def validate_password_validation_slot(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        password = tracker.get_slot("password_slot")
        if password != slot_value:
            dispatcher.utter_message("Passwords don't match.")
            return {"password_validation_slot": None}
        return {}


class SubmitNewUserForm(Action):
    def name(self) -> Text:
        return "submit_new_user_form"

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
        name = tracker.get_slot("name_slot")
        surname = tracker.get_slot("surname_slot")
        age = tracker.get_slot("age_slot")
        password = tracker.get_slot("password_slot")
        user = queries_location.find_user_by_cnp_query(cnp)

        if user:
            buttons = [
                {"payload": "/check_cnp_again_intent", "title": "I am an existing user, I want to check my CNP again."},
                {"payload": "/leave_app_intent", "title": "I wish to leave the app."},
            ]

            dispatcher.utter_button_message(
                "A user has already been found for this CNP, here are a few options:",
                buttons=buttons
            )
            return [SlotSet("cnp_slot", None)]

        queries_location.add_new_user(cnp, name, surname, age, password)
        user = queries_location.find_user_by_cnp_query(cnp)

        dispatcher.utter_message("Congratulations! user created successfully.")
        dispatcher.utter_message(f"Your new account number is: {user['account_number']}.")
        dispatcher.utter_message(f"Your current balance is: {user['balance']}.")
        return [
            SlotSet("cnp_slot", cnp),
        ]
