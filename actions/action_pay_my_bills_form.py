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

        confirm_pay_bills = tracker.get_slot("confirm_pay_bills_slot")

        if confirm_pay_bills == 'nothing_to_pay':
            dispatcher.utter_message(text="You have no bills to pay.")
            return [SlotSet('confirm_pay_bills_slot', None)]

        if not confirm_pay_bills:
            dispatcher.utter_message(text='Transaction canceled.')
            return [SlotSet('confirm_pay_bills_slot', None)]
        elif confirm_pay_bills:
            last_action = ''
            for event in reversed(tracker.events):
                if event["event"] == "action":
                    last_action = event["name"]
                    break

            cnp = tracker.get_slot("cnp_slot")
            user_balance = queries_location.get_balance_by_cnp_query(cnp)
            amount_to_be_paid = 0

            if last_action == "pay_my_bills_form":
                amount_to_be_paid = queries_location.get_total_sum_of_bills_query(cnp)
                query = queries_location.pay_bills_query
            elif last_action == "pay_my_gas_bill_form":
                amount_to_be_paid = queries_location.get_gas_bill_query(cnp)
                query = queries_location.pay_gas_bill_query
            elif last_action == "pay_my_electricity_bill_form":
                amount_to_be_paid = queries_location.get_electricity_bill_query(cnp)
                query = queries_location.pay_electricity_bill_query
            elif last_action == "pay_my_water_bill_form":
                amount_to_be_paid = queries_location.get_water_bill_query(cnp)
                query = queries_location.pay_water_bill_query
            elif last_action == "pay_my_rent_bill_form":
                amount_to_be_paid = queries_location.get_rent_bill_query(cnp)
                query = queries_location.pay_rent_bill_query
            else:
                dispatcher.utter_message(text='Something went wrong.')
                return [SlotSet('confirm_pay_bills_slot', None)]

            if user_balance >= amount_to_be_paid:
                query(cnp, amount_to_be_paid)
                dispatcher.utter_message(text='Payment successful.')
                dispatcher.utter_message(text=f"Amount paid: {amount_to_be_paid}$")
                return [SlotSet('confirm_pay_bills_slot', None)]
            else:
                dispatcher.utter_message(text="Insufficient funds. Payment not successful.")
                return [SlotSet('confirm_pay_bills_slot', None)]
        else:
            dispatcher.utter_message(text='Something went wrong.')
            return [SlotSet('confirm_pay_bills_slot', None)]
