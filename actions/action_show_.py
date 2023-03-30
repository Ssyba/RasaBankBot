from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import queries_location


class ActionShowMyCNP(Action):
    def name(self) -> Text:
        return "action_show_my_cnp"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        logged_in = tracker.get_slot("logged_in_status_slot")
        cnp = tracker.get_slot("cnp_slot")

        if logged_in:
            message = f"Your CNP is {cnp}."
        else:
            message = "You are not logged in."

        dispatcher.utter_message(text=message)
        return []


class ActionShowUserInfo(Action):
    def name(self) -> Text:
        return "action_show_user_info"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        cnp = tracker.get_slot("cnp_slot")
        user = queries_location.find_user_by_cnp_query(cnp)

        if user:
            cnp = user["CNP"]
            name = user["name"]
            surname = user["surname"]
            age = user["age"]
            account_number = user["account_number"]
            register_date = user["register_date"]
            balance = user["balance"]

            message = f"User Information:\n" \
                      f"CNP: {cnp}\n" \
                      f"Name: {name}\n" \
                      f"Surname: {surname}\n" \
                      f"Age: {age}\n" \
                      f"Account Number: {account_number}\n" \
                      f"Register Date: {register_date}\n" \
                      f"Balance: {balance}"

            dispatcher.utter_message(message)
        else:
            dispatcher.utter_message("You are not logged in.")

        return []


class ActionShowName(Action):
    def name(self) -> Text:
        return "action_show_name"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        logged_in = tracker.get_slot('logged_in_status_slot')
        cnp = tracker.get_slot('cnp_slot')

        if logged_in:
            user = queries_location.find_user_by_cnp_query(cnp)
            name = user['name']
            message = f"Your name is {name}."
        else:
            message = "You are not logged in."

        dispatcher.utter_message(text=message)
        return []


class ActionShowSurname(Action):
    def name(self) -> Text:
        return "action_show_surname"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        logged_in = tracker.get_slot('logged_in_status_slot')
        cnp = tracker.get_slot('cnp_slot')

        if logged_in:
            user = queries_location.find_user_by_cnp_query(cnp)
            surname = user['surname']
            message = f"Your surname is {surname}."
        else:
            message = "You are not logged in."

        dispatcher.utter_message(text=message)
        return []


class ActionShowAge(Action):
    def name(self) -> Text:
        return "action_show_age"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        logged_in = tracker.get_slot('logged_in_status_slot')
        cnp = tracker.get_slot('cnp_slot')

        if logged_in:
            user = queries_location.find_user_by_cnp_query(cnp)
            age = user['age']
            message = f"Your age is {age}."
        else:
            message = "You are not logged in."

        dispatcher.utter_message(text=message)
        return []


class ActionShowAccountNumber(Action):
    def name(self) -> Text:
        return "action_show_account_number"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        logged_in = tracker.get_slot('logged_in_status_slot')
        cnp = tracker.get_slot('cnp_slot')

        if logged_in:
            user = queries_location.find_user_by_cnp_query(cnp)
            account_number = user['account_number']
            message = f"Your account number is {account_number}."
        else:
            message = "You are not logged in."

        dispatcher.utter_message(text=message)
        return []


class ActionShowRegisterDate(Action):
    def name(self) -> Text:
        return "action_show_register_date"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        logged_in = tracker.get_slot('logged_in_status_slot')
        cnp = tracker.get_slot('cnp_slot')

        if logged_in:
            user = queries_location.find_user_by_cnp_query(cnp)
            register_date = user['register_date']
            message = f"Your registration date is {register_date}."
        else:
            message = "You are not logged in."

        dispatcher.utter_message(text=message)
        return []


class ActionShowBalance(Action):
    def name(self) -> Text:
        return "action_show_balance"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        logged_in = tracker.get_slot('logged_in_status_slot')
        cnp = tracker.get_slot('cnp_slot')

        if logged_in:
            balance = queries_location.get_balance_by_cnp(cnp)
            message = f"Your current balance is ${balance}."
        else:
            message = "You are not logged in."

        dispatcher.utter_message(text=message)
        return []


class ActionPrintSlots(Action):

    def name(self) -> Text:
        return "action_show_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        slots = tracker.slots
        dispatcher.utter_message(str(slots))
        return []
