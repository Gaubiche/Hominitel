import time

from display.display_registry import DisplayRegistry
from display.template_element import TemplateElement
from home_assistant.light import Light
from tab import Tab
from home_assistant.home_assistant import HomeAssistantAPI

class Dashboard(Tab):
    def __init__(self, minitel):
        super().__init__(minitel, description="Home Assistant Dashboard")
        self.api = HomeAssistantAPI()
        self.entities = []
        self.entities.append(Light("light.salon"))
        self.display_registry = DisplayRegistry()
        for entity in self.entities:
            self.display_registry.register(TemplateElement(self.minitel, entity.get_state_string, entity.get_boolean_state))

    def run(self):
        self.minitel.cls()
        self.display_registry.display()
        while True:
            self.display_registry.update()
            if self.should_stop:
                return
            time.sleep(0.1)