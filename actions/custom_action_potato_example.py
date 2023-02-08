from rasa_sdk import Action


class CapturePotatoExample(Action):
    def name(self):
        return "action_capture_potato_example"

    def run(self, dispatcher, tracker, domain):
        print("inside the potato example class")
        intent = tracker.latest_message.get("intent").get("name")
        if intent == "potato_example":
            response = "tomato"
        dispatcher.utter_message(text=response)
        return []
