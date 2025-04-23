import time

from display.display_registry import DisplayRegistry
from display.template_element import TemplateElement
from tab import Tab
from api.home_assistant import HomeAssistantAPI

class Dashboard(Tab):
    def __init__(self, minitel):
        super().__init__(minitel, description="Home Assistant Dashboard")
        self.api = HomeAssistantAPI()
        self.display_registry = DisplayRegistry()
        self.display_registry.register(TemplateElement(self.minitel,self.api.get_state))

    def run(self):
        self.minitel.cls()
        self.display_registry.display()
        while True:
            if self.should_stop:
                return
            time.sleep(0.1)