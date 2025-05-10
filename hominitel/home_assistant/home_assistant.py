from requests import get, post

from hominitel.config import config
from hominitel.minitel.connection import WiFiConnection

class HomeAssistantAPI:
    def __init__(self):
        self.api_url = config.HA_API_URL
        self.api_token = config.HA_API_TOKEN
        self.wifi_connection = WiFiConnection()
        self.wifi_connection.connect()

    def get_state(self, entity_id="light.salon"):
        url = f"{self.api_url}/states/{entity_id}"
        headers = {
            "Authorization": self.api_token,
            "content-type": "application/json",
        }
        response = get(url, headers=headers)
        return response.json()

    def set_state(self, entity_id, domain, service, data={}):
        url = f"{self.api_url}/services/{domain}/{service}"
        headers = {
            "Authorization": self.api_token,
            "content-type": "application/json",
        }
        data["entity_id"] = entity_id
        response = post(url, headers=headers, json=data)
        return response.json()

    def prompt(self, text, conversation_id=None):
        url = f"{self.api_url}/services/conversation/process"
        payload = {
            "text": text.lower(),
            "agent_id": "conversation.chatgpt"
        }
        if conversation_id is not None:
            payload["conversation_id"]= conversation_id

        headers = {
            'Content-Type': 'text/plain',
            'Authorization': self.api_token
        }
        response = post(url, headers=headers, json=payload)
        return response.json()

home_assistant_api = HomeAssistantAPI()