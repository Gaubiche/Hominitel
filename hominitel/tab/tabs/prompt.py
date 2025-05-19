import time

from hominitel.minitel.minitel import minitel
from hominitel.tab.tab import Tab


class Prompt(Tab):
    def __init__(self):
        super().__init__(description="Prompt Mode for Home Assistant")

    def run(self):
        minitel.cls()
        minitel.print("Bonjour, je suis ChatGPT")
        while True:
            time.sleep(0.1)

class HomeAssistantAPI:
    def __init__(self, url: str, token: str):
        self.url = url
        self.token = token
        self.conversation_id = None
    
    def send_command(self, text: str, language: str = "fr") -> str:
        pass
        
    def print(self, message: str, is_assistant: bool = False):
        if is_assistant:
            minitel.pos(self.line, 10)
        minitel.print("> " + message)
        print(len("> " + message))
        print("> " + message)
        self.line += 2 + (len(message) + (10 if is_assistant else 0))//40
        minitel.vtab(self.line)
    
    def wait_for_input(self):
        last_char = minitel.get_input()
        buffer = ""
        while '\r' not in str(last_char):
            if last_char == '\x13E':
                buffer = ""
                minitel.vtab(self.line)
                minitel._del(self.line, 1)
                minitel.print("> ")
            minitel.cursor(True)
            last_char = minitel.get_input()
            if last_char is not None:
                if isinstance(last_char, bytes):
                    last_char = last_char.decode('utf-8')
                buffer += last_char
            time.sleep(1)
        self.line += 2
        minitel.vtab(self.line)
        return buffer

        
if __name__ == "__main__":

    while(True):
        buffer = minitel.wait_for_input()
        minitel.clear_and_display(buffer)
        response = home_assistant_api.send_command(buffer)
        minitel.print(str(response["response"]["speech"]["plain"]["speech"]), True)

