from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, ActiveLoop
from dateutil.parser import parse
import queries_location


class ActionSetConfirmPayBillsSlot(Action):
    def name(self) -> Text:
        return "action_set_confirm_pay_bills_slot"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        cnp = tracker.get_slot("cnp_slot")
        last_action = None

        for event in reversed(tracker.events):
            if event["event"] == "action":
                last_action = event["name"]
                break

        if last_action == "action_show_my_gas_bill":
            bill_amount = queries_location.get_gas_bill_query(cnp)
        elif last_action == "action_show_my_electricity_bill":
            bill_amount = queries_location.get_electricity_bill_query(cnp)
        elif last_action == "action_show_my_water_bill":
            bill_amount = queries_location.get_water_bill_query(cnp)
        elif last_action == "action_show_my_rent_bill":
            bill_amount = queries_location.get_rent_bill_query(cnp)
        elif last_action == "action_show_my_bills":
            bill_amount = queries_location.get_total_sum_of_bills_query(cnp)
        else:
            dispatcher.utter_message(text="Invalid last action.")
            return [SlotSet("confirm_pay_bills_slot", None), ActiveLoop(None)]

        if bill_amount == 0:
            return [SlotSet("confirm_pay_bills_slot", "nothing_to_pay"), ActiveLoop(None)]
        else:
            return [SlotSet("confirm_pay_bills_slot", None), ActiveLoop(None)]


class ActionExtractTransactionDate(Action):
    def name(self) -> Text:
        return "action_extract_transaction_date"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        date_entity = next(tracker.get_latest_entity_values("transaction_date_slot"), None)

        return [SlotSet("transaction_date_slot", date_entity)]


class ActionExtractAccountNumber(Action):
    def name(self) -> Text:
        return "action_extract_account_number"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        account_number_entity = next(tracker.get_latest_entity_values("extracted_account_number_slot"), None)
        return [SlotSet("extracted_account_number_slot", account_number_entity)]
