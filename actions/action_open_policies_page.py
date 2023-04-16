from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import webbrowser
import logging

logger = logging.getLogger(__name__)


class ActionOpenWebPage(Action):
    def name(self) -> Text:
        return "action_open_policies_page"

    async def run(self,
                  dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        firefox = webbrowser.Mozilla("C:\\Program Files\\Mozilla Firefox\\firefox.exe")
        firefox.open_new_tab("file:///C:/Users/Marius/PycharmProjects/RasaBankBot/frontend/policies_page.html")
        return []
