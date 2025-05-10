import time

from hominitel.minitel.minitel import minitel
from hominitel.renderer.render_registry import RenderRegistry
from hominitel.renderer.template_element import TemplateElement
from hominitel.tab.tab import Tab

class Menu(Tab):
    def __init__(self, tabs):
        super().__init__(description="Main menu")
        self.display_registry = RenderRegistry()
        self.tabs = tabs
        self.display_registry.register(TemplateElement("Main menu"))
        for key, tab in self.tabs.items():
            self.display_registry.register(TemplateElement(f"{key}: {tab.description}\n"))

    def run(self):
        minitel.cls()
        self.display_registry.display()
        while True:
            time.sleep(1)
            if self.should_stop:
                return
