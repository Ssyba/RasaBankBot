from rasa_sdk import Action
from rasa_sdk.events import AllSlotsReset


class ActionRestart(Action):
    def name(self) -> str:
        return "action_restart"

    async def run(self, dispatcher, tracker, domain):
        return [AllSlotsReset()]
