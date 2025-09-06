import gc
from hominitel.requests import get, post
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
        """Get entity state"""
        try:            
            url = f"{self.api_url}/states/{entity_id}"
            headers = {
                "Authorization": self.api_token,
                "content-type": "application/json",
            }
            
            response = get(url, headers=headers)
            data = response.json()
            response.close()
            
            return data
        except Exception as e:
            print(f"Error getting state for {entity_id}: {e}")
            
            raise

    def set_state(self, entity_id, domain, service, data={}):
        """Set entity state with memory management"""
        try: 
            url = f"{self.api_url}/services/{domain}/{service}"
            headers = {
                "Authorization": self.api_token,
                "content-type": "application/json",
            }
            
            # Create minimal payload to reduce memory usage
            payload = {"entity_id": entity_id}
            if data:
                payload.update(data)
                
            response = post(url, headers=headers, json_data=payload)
            result = response.json()
            response.close()
            
            return result
            
        except Exception as e:
            print(f"Error setting state for {entity_id}: {e}")
            gc.collect()
            raise

    def prompt(self, text):
        """Process conversation with memory management"""
        try:
            url = f"{self.api_url}/conversation/process"
            payload = {
                "text": text.lower()
            }
            if self.conversation_id is not None:
                payload["conversation_id"] = self.conversation_id

            headers = {
                'Content-Type': 'text/plain',
                'Authorization': self.api_token
            }
            
            response = post(url, headers=headers, json_data=payload)
            response_json = response.json()
            response.close()
            
            # Extract conversation_id safely
            if "conversation_id" in response_json:
                self.conversation_id = response_json["conversation_id"]
            
            # Extract speech safely with fallback
            speech = ""
            try:
                speech = response_json.get("response", {}).get("speech", {}).get("plain", {}).get("speech", "")
            except (KeyError, TypeError):
                speech = "Error processing response"
            return speech
        except Exception as e:
            print(f"Error in conversation: {e}")
            gc.collect()
            return "Error processing request"


# Global instance with memory management
home_assistant_api = HomeAssistantAPI()
