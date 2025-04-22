from display.display_registry import DisplayRegistry
from display.template_element import TemplateElement
from tab import Tab

class Menu(Tab):
    def __init__(self, minitel, tabs):
        super().__init__(minitel, description="Main menu")
        self.display_registry = DisplayRegistry()
        self.tabs = tabs

    def run(self):
        self.display_registry.register(TemplateElement(self.minitel,"Main menu"))
        for key, tab in self.tabs.items():
            self.display_registry.register(TemplateElement(self.minitel,f"{key}: {tab.description}\n"))
        self.display_registry.display()
        while True:
            if self.should_stop:
                return
