from abc import ABC, abstractmethod
from typing import Dict, Text, Any, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import EventType, AllSlotsReset, ActiveLoop, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction


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
        # Check if logout_intent or break_intent is detected
        if tracker.latest_message['intent'].get('name') in ['logout_intent', 'break_intent']:
            cnp = tracker.slots.get('cnp_slot')
            if cnp and (len(cnp) == 4 and cnp.isdigit()):
                cnp_slot_value = tracker.slots['cnp_slot']
                return [AllSlotsReset(), ActiveLoop(None), SlotSet('cnp_slot', cnp_slot_value)]
            else:
                return [AllSlotsReset(), ActiveLoop(None)]
        return await super().run(dispatcher, tracker, domain)


class BaseSubmitAction(Action, ABC):
    @abstractmethod
    def name(self) -> Text:
        pass

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        if tracker.latest_message['intent'].get('name') == 'logout_intent':
            dispatcher.utter_message("You have been logged out.")
            return [AllSlotsReset(), ActiveLoop(None)]

        elif tracker.latest_message['intent'].get('name') == 'break_intent':
            dispatcher.utter_message("Action interrupted, how else can I be of service?")
            if tracker.slots.get('cnp_slot'):
                cnp_slot_value = tracker.slots['cnp_slot']
                return [AllSlotsReset(), ActiveLoop(None), SlotSet('cnp_slot', cnp_slot_value)]
            else:
                return [AllSlotsReset(), ActiveLoop(None)]

        return self.submit(dispatcher, tracker, domain)
