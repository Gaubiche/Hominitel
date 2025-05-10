import time

from hominitel.minitel.minitel import minitel
from hominitel.renderer.render_registry import RenderRegistry
from hominitel.renderer.template_element import TemplateElement
from hominitel.tab.tab import Tab


class HelloWorld(Tab):
    def __init__(self):
        super().__init__(description="Displays a 'Hello world'")
        self.display_registry = RenderRegistry()
        self.display_registry.register(TemplateElement("Hello world!"))

    def run(self):
        minitel.cls()
        self.display_registry.display()
        while True:
            if self.should_stop:
                return
            time.sleep(0.1)