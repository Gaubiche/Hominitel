import time

from hominitel.minitel.command_bar_state import CommandBarState
from hominitel.minitel.minitel import minitel
from hominitel.config import config
from hominitel.minitel.special_characters import SpecialCharacters
from hominitel.renderer.render_registry import RenderRegistry
from hominitel.home_assistant.entities_updater import EntitiesUpdater
from hominitel.home_assistant.entity_controller import EntityController
from hominitel.home_assistant.input_select_controller import InputSelectController
from hominitel.home_assistant.light_controller import LightController
from hominitel.tab.tab import Tab
from hominitel.minitel.command_bar import CommandBar

class Dashboard(Tab):
    def __init__(self):
        super().__init__(description="Home Assistant Dashboard")
        self.controllers = []
        for entity in config.DASHBOARD_TAB["entities"]:
            self.controllers.append(self.controller_from_entity(entity))
        self.selected_index = 0
        self.display_registry = RenderRegistry(top=1, bottom=40)
        self.entities_updater = EntitiesUpdater()
        self.command_bar = CommandBar()
        keymap_state = CommandBarState("default", "↑↓: Browse, Enter: Toggle")
        self.command_bar.register(keymap_state, True)
        for controller in self.controllers:
            self.display_registry.register(controller.get_template_element())
            self.entities_updater.register(controller)
        self.update_selected()

    def update_selected(self):
        for i, controller in enumerate(self.controllers):
            if i == self.selected_index:
                controller.select()
            else:
                controller.deselect()

    def run(self):
        minitel.cls()
        self.entities_updater.start()
        self.display_registry.display()
        self.command_bar.display()
        while True:
            while self.buffer:
                char = self.buffer[0]
                self.buffer = self.buffer[1:]
                if char == SpecialCharacters.ARROW_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.controllers)
                    self.update_selected()
                if char == SpecialCharacters.ARROW_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.controllers)
                    self.update_selected()
                elif char == "\r":
                    self.controllers[self.selected_index].trigger()
            self.display_registry.update()
            self.command_bar.update()
            if self.should_stop:
                self.entities_updater.running = False
                return
            time.sleep(0.1)

    def controller_from_entity(self, entity_id: str):
        if entity_id.startswith("light"):
            return LightController(entity_id)
        if entity_id.startswith("input_select"):
            return InputSelectController(entity_id)
        return EntityController(entity_id)