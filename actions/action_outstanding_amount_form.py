from typing import Any, Dict, List, Text
from rasa_sdk import Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import queries_location
from actions.base_classes import BaseFormValidationAction, BaseSubmitAction


class ValidateOutstandingAmountForm(BaseFormValidationAction):
    def name(self) -> Text:
        return "validate_outstanding_amount_form"

    async def validate_outstanding_amount_payment_slot(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        card_number = tracker.get_slot("extracted_card_number_slot")
        balance = queries_location.get_balance_query_by_card_number(
            card_number)
        outstanding_amount = queries_location.get_outstanding_amount_query_by_card_number(
            card_number)

        payment_amount = int(slot_value)

        if balance < payment_amount:
            dispatcher.utter_message("You don't have enough funds to make this payment.")
            return {"outstanding_amount_payment_slot": None}
        elif outstanding_amount < payment_amount:
            dispatcher.utter_message("You can't pay more than the outstanding amount.")
            return {"outstanding_amount_payment_slot": None}
        else:
            return {"outstanding_amount_payment_slot": payment_amount}


class ActionSubmitOutstandingAmountForm(BaseSubmitAction):
    def name(self) -> Text:
        return "submit_outstanding_amount_form"

    async def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        card_number = tracker.get_slot('extracted_card_number_slot')
        payment_amount = tracker.get_slot('outstanding_amount_payment_slot')

        queries_location.pay_outstanding_amount_query_by_card_number(card_number,
                                                                     payment_amount)

        dispatcher.utter_message("Payment successful!")

        return [SlotSet('outstanding_amount_payment_slot', None)]
