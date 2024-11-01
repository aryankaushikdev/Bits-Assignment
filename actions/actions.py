from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import datetime


class ActionCheckDeviceStatus(Action):
    def name(self) -> Text:
        return "action_check_device_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        device = tracker.get_slot("device")
        if not device:
            dispatcher.utter_message(text="Could you specify which device you're having issues with?")
            return []

        # Check the device status
        device_status = self.get_device_status(device)
        if device_status["status"] == "operational":
            message = f"The {device} appears to be working normally. Are you experiencing specific issues with it?"
        else:
            message = f"I've detected an issue with the {device}. {device_status['message']}"
        
        dispatcher.utter_message(text=message)
        return [SlotSet("device", device)]

    def get_device_status(self, device: Text) -> Dict[str, str]:
        # Mock implementation for demonstration
        return {
            "status": "operational",
            "message": "All systems functioning normally."
        }


class ActionCreateSupportTicket(Action):
    def name(self) -> Text:
        return "action_create_support_ticket"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        issue_type = tracker.get_slot("issue_type")
        device = tracker.get_slot("device")
        software = tracker.get_slot("software")
        
        # Create ticket details
        ticket_details = {
            "timestamp": datetime.datetime.now().isoformat(),
            "issue_type": issue_type,
            "device": device,
            "software": software,
            "conversation_id": tracker.sender_id
        }
        
        # Simulate ticket creation
        ticket_number = self.create_ticket(ticket_details)
        
        message = f"I've created support ticket #{ticket_number} for your issue. An IT support specialist will review it shortly."
        dispatcher.utter_message(text=message)
        
        return []

    def create_ticket(self, details: Dict[str, Any]) -> str:
        # Mock implementation for demonstration
        return "INC" + datetime.datetime.now().strftime("%Y%m%d%H%M")


class ActionCheckSoftwareCompatibility(Action):
    def name(self) -> Text:
        return "action_check_software_compatibility"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        software = tracker.get_slot("software")
        if not software:
            dispatcher.utter_message(text="Which software are you trying to install?")
            return []
        
        # Check compatibility
        compatibility = self.check_compatibility(software)
        if compatibility["compatible"]:
            message = f"{software} is compatible with your system. Would you like installation instructions?"
        else:
            message = f"There might be compatibility issues with {software}. {compatibility['message']}"
        
        dispatcher.utter_message(text=message)
        return [SlotSet("software", software)]

    def check_compatibility(self, software: Text) -> Dict[str, Any]:
        # Mock implementation for demonstration
        return {
            "compatible": True,
            "message": "System meets all requirements."
        }


class ActionCheckNetworkStatus(Action):
    def name(self) -> Text:
        return "action_check_network_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Simulate checking network status
        network_status = self.get_network_status()
        
        if network_status["status"] == "operational":
            message = "All network systems are currently operational. Are you experiencing specific connectivity issues?"
        else:
            message = f"We're experiencing some network issues: {network_status['message']}"
        
        dispatcher.utter_message(text=message)
        return []

    def get_network_status(self) -> Dict[str, str]:
        # Mock implementation for demonstration
        return {
            "status": "operational",
            "message": "All networks functioning normally."
        }
