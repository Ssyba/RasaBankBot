from typing import Any, Dict, List, Text
from rasa_sdk import Tracker
from rasa_sdk.events import AllSlotsReset, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import queries_location
from actions.base_classes import BaseFormValidationAction, BaseSubmitAction
from general_methods import is_valid_account_number, is_valid_transfer_amount, skip_validate_if_logged_out, \
    only_works_if_logged_in, handle_break_and_logout_special_intents
import re


class ValidateTransferFundsForm(BaseFormValidationAction):
    def name(self) -> Text:
        return "validate_transfer_funds_form"

    @skip_validate_if_logged_out
    @handle_break_and_logout_special_intents
    async def validate_recipient_account_number_slot(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        if is_valid_account_number(slot_value):
            user_cnp = tracker.get_slot("cnp_slot")
            user_account_number = queries_location.get_account_number_by_cnp_query(
                user_cnp)  # Replace this with your method to get the user's account number by CNP

            if slot_value == user_account_number:
                dispatcher.utter_message(
                    "The provided account number is the same as your account number. "
                    "Please provide a different account number in order to transfer funds.")
                return {"recipient_account_number_slot": None}
            elif queries_location.find_user_by_account_number_query(slot_value):
                return {"recipient_account_number_slot": slot_value}
            else:
                dispatcher.utter_message("We were unable to find the specified account number, please try again.")
                return {"recipient_account_number_slot": None}
        else:
            dispatcher.utter_message("Account numbers are exactly 6 characters long, pls try again.")
            return {"recipient_account_number_slot": None}

    async def validate_transfer_amount_slot(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        pattern = r'^\d+(\.\d{1,2})?(\s*\$)?$'
        match = re.match(pattern, slot_value)

        if match:
            # Remove any non-digit characters, e.g., $ sign and spaces
            amount = re.sub(r'[^\d.]', '', slot_value)
            return {"transfer_amount_slot": amount}
        else:
            dispatcher.utter_message(
                text="Invalid input. Please try again to enter the amount in dollars with up to maximum two decimal "
                     "places, e.g., '25', '25.00', '25$' or '25.00$'.")
            return {"transfer_amount_slot": None}

        cnp = tracker.get_slot("cnp_slot")
        transfer_amount = re.sub(r'[^\d.]', '', slot_value)
        if is_valid_transfer_amount(transfer_amount, cnp):
            cnp = tracker.get_slot("cnp_slot")
            current_balance = queries_location.get_balance_by_cnp_query(cnp)
            recipient_account_number = tracker.get_slot("recipient_account_number_slot")
            transfer_amount = tracker.get_slot("transfer_amount_slot")

            dispatcher.utter_message(text="Transactional information:")
            dispatcher.utter_message(text=f"Your current balance is: {current_balance} $")
            dispatcher.utter_message(text=f"Amount to be transferred: {transfer_amount} $")
            dispatcher.utter_message(text=f"Recipient's account number: {recipient_account_number}")

            return {"transfer_amount_slot": transfer_amount}
        else:
            dispatcher.utter_message(
                text="Invalid amount. Please make sure you entered only digits and that you have enough funds.")
            return {"transfer_amount": None}

    async def validate_confirm_transfer_slot(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        intent = tracker.latest_message['intent'].get('name')
        if intent == 'affirm_intent':
            return {"confirm_transfer_slot": True}
        elif intent == 'deny_intent':
            return {"confirm_transfer_slot": False}


class ActionSubmitTransferFundsForm(BaseSubmitAction):
    def name(self) -> Text:
        return "submit_transfer_funds_form"

    @only_works_if_logged_in
    async def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        cnp = tracker.get_slot("cnp_slot")
        recipient_account_number = tracker.get_slot("recipient_account_number_slot")
        transfer_amount = tracker.get_slot("transfer_amount_slot")
        confirm_transfer = tracker.get_slot("confirm_transfer_slot")

        if confirm_transfer:
            queries_location.transfer_funds_query(cnp, recipient_account_number, transfer_amount)
            updated_balance = queries_location.get_balance_by_cnp_query(cnp)

            dispatcher.utter_message(text="Transfer successful!")
            dispatcher.utter_message(text=f"Amount transferred: {transfer_amount}")
            dispatcher.utter_message(text=f"Recipient's account number: {recipient_account_number}")
            dispatcher.utter_message(text=f"Remaining balance: {updated_balance}")
        else:
            dispatcher.utter_message(text="Transfer canceled.")
        return [AllSlotsReset(), SlotSet('cnp_slot', cnp),
                SlotSet('logged_in_status_slot', True)]
