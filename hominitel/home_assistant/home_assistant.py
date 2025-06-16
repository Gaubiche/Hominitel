from requests import get, post

from hominitel.config import config
from hominitel.minitel.connection import WiFiConnection

class HomeAssistantAPI:
    def __init__(self):
        self.api_url = config.HA_API_URL
        self.api_token = config.HA_API_TOKEN
        self.wifi_connection = WiFiConnection()
        self.wifi_connection.connect()
        self.conversation_id = None

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

    def prompt(self, text):
        url = f"{self.api_url}/conversation/process"
        payload = {
            "text": text.lower()
        }
        if self.conversation_id is not None:
            payload["conversation_id"]= self.conversation_id

        headers = {
            'Content-Type': 'text/plain',
            'Authorization': self.api_token
        }
        response = post(url, headers=headers, json=payload)
        response_json = response.json()
        response.close()
        self.conversation_id = response_json["conversation_id"]
        return response_json.get("response", {}).get("speech", {}).get("plain", {}).get("speech", "")

home_assistant_api = HomeAssistantAPI()
