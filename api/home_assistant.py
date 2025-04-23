from requests import get
import config
from api.connection import WiFiConnection

class HomeAssistantAPI:
    def __init__(self):
        self.api_url = config.API_URL
        self.api_token = config.API_TOKEN
        self.wifi_connection = WiFiConnection()
        self.wifi_connection.connect()

    def get_state(self, entity_id="light.salon"):
        url = f"{self.api_url}/states/{entity_id}"
        headers = {
            "Authorization": self.api_token,
            "content-type": "application/json",
        }
        response = get(url, headers=headers)
        print(str(response.json()))
        return str(response.json())
