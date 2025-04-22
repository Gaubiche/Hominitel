import time

from display.display_registry import DisplayRegistry
from display.template_element import TemplateElement
from tab import Tab


class HelloWorld(Tab):
    def __init__(self, minitel):
        super().__init__(minitel, description="Displays a 'Hello world'")
        self.display_registry = DisplayRegistry()

    def run(self):
        self.display_registry.register(TemplateElement(self.minitel,"Hello world!"))
        while True:
            if self.should_stop:
                return
            time.sleep(0.1)