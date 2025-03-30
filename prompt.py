import network
from machine import UART
from lib import upynitel
import urequests
import time
import json
import config


class WiFiConnection:
    def __init__(self, ssid: str, password: str, minitel: Minitel):
        self.ssid = ssid
        self.password = password
        self.wlan = network.WLAN(network.STA_IF)
        self.minitel = minitel
    
    def connect(self):
        self.wlan.active(True)
        
        if not self.wlan.isconnected():
            self.minitel.print("Connecting to wifi")
            self.wlan.connect(self.ssid, self.password)

            for _ in range(10):
                if self.wlan.isconnected():
                    break
                print(".", end="")
                time.sleep(1)
        
        if not self.wlan.isconnected():
            minitel.print("\nImpossible de se connecter au Wi-Fi")
            time.sleep(10)
            raise Exception()
        
class HomeAssistantAPI:
    def __init__(self, url: str, token: str):
        self.url = url
        self.token = token
        self.conversation_id = None
    
    def send_command(self, text: str, language: str = "fr") -> str:
        """
        Sends a command to the home automation system via an HTTP POST request.

        :param text: The command to send (e.g., "turn off the living room light").
        :param language: The language of the command (default is "fr").
        :return: The server response as a string.
        """
        payload = {
            "text": text.lower(),
            "agent_id": "conversation.chatgpt"
        }
        if self.conversation_id is not None:
            payload["conversation_id"]= self.conversation_id
        print(payload)

        headers = {
            'Content-Type': 'text/plain',  
            'Authorization': f"Bearer {self.token}"  
        }
        try:
            response = urequests.post(self.url, headers=headers, data=json.dumps(payload))
            response_json = response.json()
            response.close()
            self.conversation_id = response_json.get("conversation_id", None)
            return response_json
        except Exception as e:
            return f"Error sending command: {str(e)}"

class System:
    def __init__(self):
        self.minitel = upynitel.Pynitel(UART(2, baudrate=1200, parity=0, bits=7, stop=1))
        self.minitel.cls()
        self.minitel.drawscreen('homeassistant.vtx')
        self.baseline = 4
        self.line = self.baseline
        self.minitel.vtab(self.line)
        
    def print(self, message: str, is_assistant: bool = False):
        if is_assistant:
            self.minitel.pos(self.line, 10)
        self.minitel._print("> " + message)
        print(len("> " + message))
        print("> " + message)
        self.line += 2 + (len(message) + (10 if is_assistant else 0))//40
        self.minitel.vtab(self.line)
    
    def wait_for_input(self):
        last_char = self.minitel._if()
        buffer = ""
        while '\r' not in str(last_char):
            if last_char == '\x13E':
                print(last_char)
                buffer = ""
                self.minitel.vtab(self.line)
                self.minitel._del(self.line, 1)
                self.minitel._print("> ")
            self.minitel.cursor(True)
            last_char = self.minitel._if()
            if last_char is not None:
                if isinstance(last_char, bytes):
                    print(last_char)
                    last_char = last_char.decode('utf-8')
                    print(last_char)
                buffer += last_char
            time.sleep(1)
        self.line += 2
        self.minitel.vtab(self.line)
        return buffer
    
    def text_input(self):
        self.minitel._print("> ")
        last_char = self.minitel._if()
        buffer = ""
        
        while '\r' not in str(last_char):
            if last_char == '\x13E':
                print(last_char)
                buffer = ""
                self.minitel.vtab(self.line)
                self.minitel._del(self.line, 1)
                self.minitel._print("> ")
            self.minitel.cursor(True)
            last_char = self.minitel._if()
            if last_char is not None:
                if isinstance(last_char, bytes):
                    print(last_char)
                    last_char = last_char.decode('utf-8')
                    print(last_char)
                buffer += last_char
            time.sleep(1)
        self.line += 2
        self.minitel.vtab(self.line)
        return buffer
    
    def clear_and_display(self, message:str):
        self.minitel.cls()
        self.line = self.baseline
        self.print(message)

        
if __name__ == "__main__":
    minitel = System()
    wifi_connection = WiFiConnection(config.WIFI_SSID, config.WIFI_PASSWORD, minitel)
    home_assistant_api = HomeAssistantAPI(config.API_URL, config.API_TOKEN)
    wifi_connection.connect()
    minitel.print("Bonjour, je suis ChatGPT", True)
    while(True):
        buffer = minitel.wait_for_input()
        minitel.clear_and_display(buffer)
        response = home_assistant_api.send_command(buffer)
        minitel.print(str(response["response"]["speech"]["plain"]["speech"]), True)
        

