from datetime import datetime
from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import queries_location


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

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> \
            List[Dict[Text, Any]]:
        cnp = tracker.get_slot('cnp_slot')
        user = queries_location.find_user_by_cnp_query(cnp)
        name = user['name']

        dispatcher.utter_message(text=f"Your name is {name}.")
        return []


class ActionShowMySurname(Action):
    def name(self) -> Text:
        return "action_show_my_surname"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> \
            List[Dict[Text, Any]]:
        cnp = tracker.get_slot('cnp_slot')
        user = queries_location.find_user_by_cnp_query(cnp)
        surname = user['surname']

        dispatcher.utter_message(text=f"Your surname is {surname}.")
        return []


class ActionShowMyAge(Action):
    def name(self) -> Text:
        return "action_show_my_age"

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

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> \
            List[Dict[Text, Any]]:
        cnp = tracker.get_slot('cnp_slot')
        user = queries_location.find_user_by_cnp_query(cnp)
        balance = user['balance']

        dispatcher.utter_message(text=f"Your balance is {balance}$.")
        return []


# Bills table show #
class ActionShowMyBills(Action):
    def name(self) -> Text:
        return "action_show_my_bills"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> \
            List[Dict[Text, Any]]:
        cnp = tracker.get_slot('cnp_slot')
        user_bills = queries_location.find_bills_by_cnp_query(cnp)
        gas = user_bills['gas']
        electricity = user_bills['electricity']
        water = user_bills['water']
        rent = user_bills['rent']
        total = gas + electricity + water + rent

        dispatcher.utter_message(text="Here is a list of all your bills:")
        dispatcher.utter_message(text=f"Your gas bill is {gas}$.")
        dispatcher.utter_message(text=f"Your electricity bill is {electricity}$.")
        dispatcher.utter_message(text=f"Your water bill is {water}$.")
        dispatcher.utter_message(text=f"Your rent bill is {rent}$.")
        dispatcher.utter_message(text=f"Your total comes to {total}$.")
        return []


class ActionShowMyGasBill(Action):
    def name(self) -> Text:
        return "action_show_my_gas_bill"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> \
            List[Dict[Text, Any]]:
        cnp = tracker.get_slot('cnp_slot')
        user_bills = queries_location.find_bills_by_cnp_query(cnp)
        gas = user_bills['gas']

        dispatcher.utter_message(text=f"Your gas bill is {gas}$.")
        return []


class ActionShowMyElectricityBill(Action):
    def name(self) -> Text:
        return "action_show_my_electricity_bill"

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

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> \
            List[Dict[Text, Any]]:
        cnp = tracker.get_slot('cnp_slot')
        user_bills = queries_location.find_bills_by_cnp_query(cnp)
        rent = user_bills['rent']

        dispatcher.utter_message(text=f"Your rent bill is {rent}$.")
        return []


# Bills table show #
class ActionShowMyTransactions(Action):
    def name(self) -> Text:
        return "action_show_my_transactions"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> \
            List[Dict[Text, Any]]:
        cnp = tracker.get_slot('cnp_slot')
        user_transactions = queries_location.find_transactions_by_cnp_query(cnp)

        dispatcher.utter_message(text="Here is a list of all your transactions:")
        for trans in user_transactions:
            dispatcher.utter_message(
                text=f"Transaction ID: {trans['id']}, Type: {trans['transaction_type']}, Amount: {trans['amount']}, Date: {trans['transaction_date']}.")
        return []


class ActionShowMyTransfers(Action):
    def name(self) -> Text:
        return "action_show_my_transfers"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> \
            List[Dict[Text, Any]]:
        cnp = tracker.get_slot('cnp_slot')
        user_transfers = queries_location.find_transfers_by_cnp_query(cnp)

        if not user_transfers:
            dispatcher.utter_message(text="No transfers found.")
            return []

        dispatcher.utter_message(text="Here is a list of all your transfers:")
        for transfer in user_transfers:
            dispatcher.utter_message(
                text=f"Transfer ID: {transfer['id']}, Type: {transfer['transaction_type']}, Amount: {transfer['amount']}, Date: {transfer['transaction_date']}.")
        return []


class ActionShowMyBillPayments(Action):
    def name(self) -> Text:
        return "action_show_my_bill_payments"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> \
            List[Dict[Text, Any]]:
        cnp = tracker.get_slot('cnp_slot')
        user_bill_payments = queries_location.find_bill_payments_by_cnp_query(cnp)

        if not user_bill_payments:
            dispatcher.utter_message(text="No bill payments found.")
            return []

        dispatcher.utter_message(text="Here is a list of all your bill payments:")
        for payment in user_bill_payments:
            dispatcher.utter_message(
                text=f"Payment ID: {payment['id']}, Type: {payment['transaction_type']}, Amount: {payment['amount']}, Date: {payment['transaction_date']}.")
        return []


class ActionShowMyTransactionsByDate(Action):
    def name(self) -> Text:
        return "action_show_my_transactions_by_date"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        cnp = tracker.get_slot('cnp_slot')
        date = tracker.get_slot('transaction_date_slot')

        # Validate date format
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            dispatcher.utter_message(text="Invalid date format. Please enter a valid date (YYYY-MM-DD).")
            return [SlotSet("transaction_date_slot", None)]

        user_transactions = queries_location.find_transactions_by_cnp_and_date_query(cnp, date)

        if not user_transactions:
            dispatcher.utter_message(text="No transactions found for this date.")
            return []

        dispatcher.utter_message(text="Here are your transactions:")
        for trans in user_transactions:
            dispatcher.utter_message(
                text=f"Transaction ID: {trans['id']}, Type: {trans['transaction_type']}, Amount: {trans['amount']}, Date: {trans['transaction_date']}.")

        return []


class ActionShowMyTransfersByAccount(Action):
    def name(self) -> Text:
        return "action_show_my_transfers_by_account"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        cnp = tracker.get_slot('cnp_slot')
        account_number = tracker.get_slot('extracted_account_number_slot')

        # Validate account number
        if not account_number.isdigit() or len(account_number) != 6:
            dispatcher.utter_message(text="Invalid account number. It should be exactly 6 digits.")
            return [SlotSet("extracted_account_number_slot", None)]

        user_transfers = queries_location.find_transfers_by_cnp_and_account_number_query(cnp, account_number)

        if not user_transfers:
            dispatcher.utter_message(text="No transactions found for the specified account.")
            return []

        dispatcher.utter_message(text="Here are the transfers for the specified account:")
        for transfer in user_transfers:
            dispatcher.utter_message(
                text=f"Transfer ID: {transfer['id']}, Type: {transfer['transaction_type']}, Amount: {transfer['amount']}, Date: {transfer['transaction_date']}.")

        return []
