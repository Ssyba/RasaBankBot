from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import queries_location
from general_methods import only_works_if_logged_in


# General show #
class ActionShowAllSlots(Action):

    def name(self) -> Text:
        return "action_show_all_slots"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        slots = tracker.slots
        dispatcher.utter_message(str(slots))
        return []


# Show for users table #
class ActionShowMyUserInfo(Action):
    def name(self) -> Text:
        return "action_show_my_user_info"

    @only_works_if_logged_in
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

    @only_works_if_logged_in
    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        cnp = tracker.get_slot("cnp_slot")

        dispatcher.utter_message(text=f"Your CNP is {cnp}.")
        return []


class ActionShowMyName(Action):
    def name(self) -> Text:
        return "action_show_my_name"

    @only_works_if_logged_in
    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        cnp = tracker.get_slot('cnp_slot')
        user = queries_location.find_user_by_cnp_query(cnp)
        name = user['name']

        dispatcher.utter_message(text=f"Your name is {name}.")
        return []


class ActionShowMySurname(Action):
    def name(self) -> Text:
        return "action_show_my_surname"

    @only_works_if_logged_in
    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> \
            List[Dict[Text, Any]]:
        cnp = tracker.get_slot('cnp_slot')
        user = queries_location.find_user_by_cnp_query(cnp)
        surname = user['surname']

        dispatcher.utter_message(text=f"Your name is {surname}.")
        return []


class ActionShowMyAge(Action):
    def name(self) -> Text:
        return "action_show_my_age"

    @only_works_if_logged_in
    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> \
            List[Dict[Text, Any]]:
        cnp = tracker.get_slot('cnp_slot')
        user = queries_location.find_user_by_cnp_query(cnp)
        age = user['age']

        dispatcher.utter_message(text=f"Your age is {age}.")
        return []


class ActionShowMyAccountNumber(Action):
    def name(self) -> Text:
        return "action_show_my_account_number"

    @only_works_if_logged_in
    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> \
            List[Dict[Text, Any]]:
        cnp = tracker.get_slot('cnp_slot')
        user = queries_location.find_user_by_cnp_query(cnp)
        account_number = user['account_number']

        dispatcher.utter_message(text=f"Your account_number is {account_number}.")
        return []


class ActionShowMyRegistrationDate(Action):
    def name(self) -> Text:
        return "action_show_my_registration_date"

    @only_works_if_logged_in
    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> \
            List[Dict[Text, Any]]:
        cnp = tracker.get_slot('cnp_slot')
        user = queries_location.find_user_by_cnp_query(cnp)
        registration_date = user['registration_date']

        dispatcher.utter_message(text=f"Your account_number is {registration_date}.")
        return []


class ActionShowMyBalance(Action):
    def name(self) -> Text:
        return "action_show_my_balance"

    @only_works_if_logged_in
    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> \
            List[Dict[Text, Any]]:
        cnp = tracker.get_slot('cnp_slot')
        user = queries_location.find_user_by_cnp_query(cnp)
        balance = user['balance']

        dispatcher.utter_message(text=f"Your balance is {balance}$.")
        return []


# Bills table show #
class ActionShowMyGasBill(Action):
    def name(self) -> Text:
        return "action_show_my_bills_intent"

    @only_works_if_logged_in
    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> \
            List[Dict[Text, Any]]:
        cnp = tracker.get_slot('cnp_slot')
        user_bills = queries_location.find_bills_by_cnp_query(cnp)
        gas = user_bills['gas']
        electricity = user_bills['electricity']
        water = user_bills['water']
        rent = user_bills['rent']

        dispatcher.utter_message(text=f"Your gas bill is {gas}$.")
        dispatcher.utter_message(text=f"Your electricity bill is {electricity}$.")
        dispatcher.utter_message(text=f"Your water bill is {water}$.")
        dispatcher.utter_message(text=f"Your rent bill is {rent}$.")
        return []


class ActionShowMyGasBill(Action):
    def name(self) -> Text:
        return "action_show_my_gas_bill"

    @only_works_if_logged_in
    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        cnp = tracker.get_slot('cnp_slot')
        user_bills = queries_location.find_bills_by_cnp_query(cnp)
        gas = user_bills['gas']

        dispatcher.utter_message(text=f"Your gas bill is {gas}$.")
        return []


class ActionShowMyElectricityBill(Action):
    def name(self) -> Text:
        return "action_show_my_electricity_bill"

    @only_works_if_logged_in
    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> \
            List[Dict[Text, Any]]:
        cnp = tracker.get_slot('cnp_slot')
        user_bills = queries_location.find_bills_by_cnp_query(cnp)
        electricity = user_bills['electricity']

        dispatcher.utter_message(text=f"Your electricity bill is {electricity}$.")
        return []


class ActionShowMyWaterBill(Action):
    def name(self) -> Text:
        return "action_show_my_water_bill"

    @only_works_if_logged_in
    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> \
            List[Dict[Text, Any]]:
        cnp = tracker.get_slot('cnp_slot')
        user_bills = queries_location.find_bills_by_cnp_query(cnp)
        water = user_bills['water']

        dispatcher.utter_message(text=f"Your water bill is {water}$.")
        return []


class ActionShowMyRentBill(Action):
    def name(self) -> Text:
        return "action_show_my_rent_bill"

    @only_works_if_logged_in
    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> \
            List[Dict[Text, Any]]:
        cnp = tracker.get_slot('cnp_slot')
        user_bills = queries_location.find_bills_by_cnp_query(cnp)
        rent = user_bills['rent']

        dispatcher.utter_message(text=f"Your rent bill is {rent}$.")
        return []
