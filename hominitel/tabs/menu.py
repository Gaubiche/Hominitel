from hominitel.renderer.render_registry import RenderRegistry
from hominitel.renderer.template_element import TemplateElement
from hominitel.tab import Tab
import time

class Menu(Tab):
    def __init__(self, minitel, tabs):
        super().__init__(minitel, description="Main menu")
        self.display_registry = RenderRegistry()
        self.tabs = tabs
        self.display_registry.register(TemplateElement(self.minitel,"Main menu"))
        for key, tab in self.tabs.items():
            self.display_registry.register(TemplateElement(self.minitel,f"{key}: {tab.description}\n"))

    def run(self):
        self.minitel.cls()
        self.display_registry.display()
        while True:
            time.sleep(1)
            if self.should_stop:
                return
