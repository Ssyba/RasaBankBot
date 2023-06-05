from typing import Any, Dict, List, Text
from rasa_sdk import Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import queries_location
from actions.base_classes import BaseSubmitAction, BaseFormValidationAction


class ValidatePayMyBillsForm(BaseFormValidationAction):
    def name(self) -> Text:
        return "validate_pay_my_bills_form"

    async def validate_confirm_pay_bills_slot(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        return {'confirm_pay_bills_slot': slot_value}


class ValidatePayMyGasBillForm(BaseFormValidationAction):
    def name(self) -> Text:
        return "validate_pay_my_gas_bill_form"

    async def validate_confirm_pay_bills_slot(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        return {'confirm_pay_bills_slot': slot_value}


class ValidatePayMyElectricityBillForm(BaseFormValidationAction):
    def name(self) -> Text:
        return "validate_pay_my_electricity_bill_form"

    async def validate_confirm_pay_bills_slot(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        return {'confirm_pay_bills_slot': slot_value}


class ValidatePayMyWaterBillForm(BaseFormValidationAction):
    def name(self) -> Text:
        return "validate_pay_my_water_bill_form"

    async def validate_confirm_pay_bills_slot(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        return {'confirm_pay_bills_slot': slot_value}


class ValidatePayMyRentBillForm(BaseFormValidationAction):
    def name(self) -> Text:
        return "validate_pay_my_rent_bill_form"

    async def validate_confirm_pay_bills_slot(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        return {'confirm_pay_bills_slot': slot_value}


class ActionSubmitPayMyBillsForm(BaseSubmitAction):
    def name(self) -> Text:
        return "submit_pay_my_bills_form"

    async def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        cnp = tracker.get_slot("cnp_slot")
        confirm_pay_bills = tracker.get_slot("confirm_pay_bills_slot")

        if confirm_pay_bills == 'nothing_to_pay':
            dispatcher.utter_message(text="You have no bills to pay.")
        elif confirm_pay_bills:
            last_action = ''
            for event in reversed(tracker.events):
                if event["event"] == "action":
                    last_action = event["name"]
                    break

            user_balance = queries_location.get_balance_by_cnp_query(cnp)
            bill_action_query_map = {
                "pay_my_bills_form": (
                    "All Bills", queries_location.get_total_sum_of_bills_query, queries_location.pay_bills_query),
                "pay_my_gas_bill_form": (
                    "Gas", queries_location.get_gas_bill_query, queries_location.pay_gas_bill_query),
                "pay_my_electricity_bill_form": ("Electricity", queries_location.get_electricity_bill_query,
                                                 queries_location.pay_electricity_bill_query),
                "pay_my_water_bill_form": (
                    "Water", queries_location.get_water_bill_query, queries_location.pay_water_bill_query),
                "pay_my_rent_bill_form": (
                    "Rent", queries_location.get_rent_bill_query, queries_location.pay_rent_bill_query)
            }

            if last_action in bill_action_query_map:
                bill_type, get_bill_query, pay_bill_query = bill_action_query_map[last_action]
                amount_to_be_paid = get_bill_query(cnp)

                if user_balance >= amount_to_be_paid:
                    pay_bill_query(cnp, amount_to_be_paid)
                    queries_location.log_payment_query(cnp, bill_type, amount_to_be_paid)  # Log the transaction
                    dispatcher.utter_message(text='Payment successful.')
                    dispatcher.utter_message(text=f"Amount paid: {amount_to_be_paid}$")
                else:
                    dispatcher.utter_message(text="Insufficient funds. Payment not successful.")
            else:
                dispatcher.utter_message(text='Something went wrong.')
        else:
            dispatcher.utter_message(text='Transaction canceled.')
        return [SlotSet('confirm_pay_bills_slot', None)]
