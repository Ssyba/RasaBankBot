from typing import Any, Dict, List, Text
from rasa_sdk import Tracker
from rasa_sdk.events import AllSlotsReset, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import queries_location
from actions.base_classes import BaseSubmitAction, BaseFormValidationAction
from general_methods import skip_validate_if_logged_out, \
    handle_break_and_logout_special_intents, only_works_if_logged_in


class ValidatePayMyBillsForm(BaseFormValidationAction):
    def name(self) -> Text:
        return "validate_pay_my_bills_form"

    @skip_validate_if_logged_out
    @handle_break_and_logout_special_intents
    async def validate_confirm_pay_bills_slot(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        return await super().validate_confirm_pay_bills_slot_common(slot_value, dispatcher, tracker, domain)


class ActionSubmitPayMyBillsForm(BaseSubmitAction):
    def name(self) -> Text:
        return "submit_pay_my_bills_form"

    @only_works_if_logged_in
    async def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        confirm_pay_bills = tracker.get_slot("confirm_pay_bills_slot")
        cnp = tracker.get_slot("cnp_slot")

        if confirm_pay_bills != 'nothing_to_pay':
            user_balance = queries_location.get_balance_by_cnp_query(cnp)
            amount_to_be_paid = queries_location.get_total_sum_of_bills_query(cnp)

            if user_balance >= amount_to_be_paid:
                queries_location.pay_bills_query(cnp, amount_to_be_paid)
                dispatcher.utter_message(text='Payment successful.')
                dispatcher.utter_message(text=f"Amount paid: {amount_to_be_paid}$")
                return []
            else:
                dispatcher.utter_message(text="Insufficient funds. Payment not successful.")
                return [AllSlotsReset(), SlotSet('cnp_slot', cnp), SlotSet('logged_in_status_slot', True)]
        else:
            dispatcher.utter_message(text="You have no bills to pay.")

        return [AllSlotsReset(), SlotSet('cnp_slot', cnp), SlotSet('logged_in_status_slot', True)]
