from abc import ABC, abstractmethod
from typing import Dict, Text, Any, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import EventType, AllSlotsReset, ActiveLoop, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict

from general_methods import skip_validate_if_logged_out, handle_break_and_logout_special_intents


class BaseFormValidationAction(FormValidationAction, ABC):
    @abstractmethod
    def name(self) -> Text:
        pass

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[EventType]:
        if tracker.latest_message['intent'].get('name') in ['logout_intent', 'break_intent']:
            return [SlotSet("requested_slot", None)]
        return await super().run(dispatcher, tracker, domain)

    @skip_validate_if_logged_out
    @handle_break_and_logout_special_intents
    async def validate_confirm_pay_bills_slot_common(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        intent = tracker.latest_message["intent"].get("name")
        if intent == "affirm":
            return {'confirm_pay_bills_slot': True}
        elif intent == "deny":
            return {'confirm_pay_bills_slot': False}


class BaseSubmitAction(Action, ABC):
    @abstractmethod
    def name(self) -> Text:
        pass

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        if tracker.latest_message['intent'].get('name') == 'logout_intent':
            dispatcher.utter_message("You have been logged out.")
            return [ActiveLoop(None), AllSlotsReset()]

        elif tracker.latest_message['intent'].get('name') == 'break_intent':
            cnp_slot_value = tracker.slots['cnp_slot']
            logged_in_status = tracker.slots['logged_in_status_slot']
            dispatcher.utter_message("Action interrupted, how else can I be of service?")
            if logged_in_status:
                return [ActiveLoop(None), AllSlotsReset(), SlotSet('cnp_slot', cnp_slot_value),
                        SlotSet('logged_in_status_slot', logged_in_status)]
            else:
                return [ActiveLoop(None), AllSlotsReset()]

        return await self.submit(dispatcher, tracker, domain)
