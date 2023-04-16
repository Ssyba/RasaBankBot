from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import queries_location
from general_methods import message_for_logged_out


class ActionShowUserInfo(Action):
    def name(self) -> Text:
        return "action_show_my_user_info"

    @message_for_logged_out
    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        cnp = tracker.get_slot("cnp_slot")
        user = queries_location.find_user_by_cnp_query(cnp)

        cnp = user["CNP"]
        name = user["name"]
        surname = user["surname"]
        age = user["age"]
        account_number = user["account_number"]
        registration_date = user["registration_date"]
        balance = user["balance"]

        dispatcher.utter_message(text=f"User Information:")
        dispatcher.utter_message(text=f"CNP: {cnp}")
        dispatcher.utter_message(text=f"Name: {name}")
        dispatcher.utter_message(text=f"Surname: {surname}")
        dispatcher.utter_message(text=f"Age: {age}")
        dispatcher.utter_message(text=f"Account Number: {account_number}")
        dispatcher.utter_message(text=f"registration Date: {registration_date}")
        dispatcher.utter_message(text=f"Balance: {balance}$")

        return []


class ActionShowMyCNP(Action):
    def name(self) -> Text:
        return "action_show_my_cnp"

    @message_for_logged_out
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


class ActionShowName(Action):
    def name(self) -> Text:
        return "action_show_my_name"

    @message_for_logged_out
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
        return "action_show_my_surname"

    @message_for_logged_out
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
        return "action_show_my_age"

    @message_for_logged_out
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
        return "action_show_my_account_number"

    @message_for_logged_out
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


class ActionShowRegistrationDate(Action):
    def name(self) -> Text:
        return "action_show_my_registration_date"

    @message_for_logged_out
    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        logged_in = tracker.get_slot('logged_in_status_slot')
        cnp = tracker.get_slot('cnp_slot')

        if logged_in:
            user = queries_location.find_user_by_cnp_query(cnp)
            registration_date = user['registration_date']
            message = f"Your registration date is {registration_date}."
        else:
            message = "You are not logged in."

        dispatcher.utter_message(text=message)
        return []


class ActionShowBalance(Action):
    def name(self) -> Text:
        return "action_show_my_balance"

    @message_for_logged_out
    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        logged_in = tracker.get_slot('logged_in_status_slot')
        cnp = tracker.get_slot('cnp_slot')

        if logged_in:
            balance = queries_location.get_balance_by_cnp_query(cnp)
            message = f"Your current balance is ${balance}."
        else:
            message = "You are not logged in."

        dispatcher.utter_message(text=message)
        return []


class ActionPrintSlots(Action):

    def name(self) -> Text:
        return "action_show_slots"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        slots = tracker.slots
        dispatcher.utter_message(str(slots))
        return []
