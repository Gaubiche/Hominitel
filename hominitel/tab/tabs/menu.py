import time

from hominitel.controller.selectable import Selectable
from hominitel.minitel.command_bar import command_bar
from hominitel.minitel.minitel import minitel
from hominitel.minitel.special_characters import SpecialCharacters
from hominitel.renderer.render_registry import RenderRegistry
from hominitel.renderer.template_element import TemplateElement
from hominitel.tab.tab import Tab

class Menu(Tab):
    def __init__(self, tabs):
        super().__init__(description="Main menu")
        self.display_registry = RenderRegistry()
        self.selected_index = 0
        self.controllers = []
        self.tab_names = []
        self.display_registry.register(TemplateElement("Main menu"))
        for i, (name, tab) in enumerate(tabs.items()):
            controller = Selectable(f"{name}: {tab.description}\n")
            self.tab_names.append(name)
            self.display_registry.register(controller.get_template_element())
            self.controllers.append(controller)
        self.update_selected()

    def update_selected(self):
        for i, controller in enumerate(self.controllers):
            if i == self.selected_index:
                controller.select()
            else:
                controller.deselect()

    def run(self):
        minitel.cls()
        command_bar.set_state("menu-default")
        self.display_registry.display()
        while True:
            while self.buffer:
                char = self.buffer[0]
                self.buffer = self.buffer[1:]
                self.on_key(char)
            self.display_registry.update()
            if self.should_stop:
                return
            time.sleep(0.1)

    def on_key(self, char):
        if char == SpecialCharacters.ARROW_DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.controllers)
            self.update_selected()
        if char == SpecialCharacters.ARROW_UP:
            self.selected_index = (self.selected_index - 1) % len(self.controllers)
            self.update_selected()
        elif char == SpecialCharacters.ENTER:
            self.should_stop = True
            self.next_tab = self.tab_names[self.selected_index]
