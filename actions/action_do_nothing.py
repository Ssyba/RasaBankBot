# from typing import Any, Text, Dict, List
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionIgnoreGreet(Action):
#     def name(self) -> Text:
#         return "action_do_nothing"
#
#     async def run(
#             self,
#             dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]
#     ) -> List[Dict[Text, Any]]:
#         # Do nothing
#         return []
