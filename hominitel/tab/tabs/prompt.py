import time

from hominitel.tab.tab import Tab


class Prompt(Tab):
    def __init__(self, minitel):
        super().__init__(minitel, description="Prompt Mode for Home Assistant")

    def run(self):
        self.minitel.cls()
        self.minitel._print("Bonjour, je suis ChatGPT")
        while True:
            while self.buffer!= "":
                char = self.buffer[0]
                self.buffer = self.buffer[1:]
                if char == " ":
                    self.selected_index = (self.selected_index + 1) % len(self.controllers)
                    self.update_selected()
                elif char == "\r":
                    self.controllers[self.selected_index].trigger()
            self.display_registry.update()
            if self.should_stop:
                self.entities_updater.running = False
                return
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
                buffer = ""
                self.minitel.vtab(self.line)
                self.minitel._del(self.line, 1)
                self.minitel._print("> ")
            self.minitel.cursor(True)
            last_char = self.minitel._if()
            if last_char is not None:
                if isinstance(last_char, bytes):
                    last_char = last_char.decode('utf-8')
                buffer += last_char
            time.sleep(1)
        self.line += 2
        self.minitel.vtab(self.line)
        return buffer

        
if __name__ == "__main__":

    while(True):
        buffer = minitel.wait_for_input()
        minitel.clear_and_display(buffer)
        response = home_assistant_api.send_command(buffer)
        minitel.print(str(response["response"]["speech"]["plain"]["speech"]), True)

