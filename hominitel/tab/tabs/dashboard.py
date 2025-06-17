import time

from hominitel.minitel.minitel import minitel
from hominitel.config import config
from hominitel.minitel.special_characters import SpecialCharacters
from hominitel.renderer.render_registry import RenderRegistry
from hominitel.home_assistant.entities_updater import EntitiesUpdater
from hominitel.home_assistant.entity_controller import EntityController
from hominitel.home_assistant.input_select_controller import InputSelectController
from hominitel.home_assistant.light_controller import LightController
from hominitel.home_assistant.notification_monitor import NotificationMonitor
from hominitel.tab.tab import Tab
from hominitel.minitel.command_bar import command_bar


class Dashboard(Tab):
    def __init__(self):
        super().__init__(description="Home Assistant Dashboard")
        self.controllers = []
        for entity in config.DASHBOARD_TAB["entities"]:
            self.controllers.append(self.controller_from_entity(entity))
        self.state_actions = {
            "default": self.default,
            "navigation": self.navigation,
        }
        self.display_registry = RenderRegistry(top=1, bottom=40)
        self.entities_updater = EntitiesUpdater()
        for controller in self.controllers:
            self.display_registry.register(controller.get_template_element())
            self.entities_updater.register(controller)
        self.selected_index = 0
        self.update_selected()
        self.current_state = "default"
        
        # Initialize notification monitor
        self.notification_monitor = NotificationMonitor()

    def update_selected(self):
        for i, controller in enumerate(self.controllers):
            if i == self.selected_index:
                controller.select()
            else:
                controller.deselect()

    def run(self):
        self.should_stop = False
        self.selected_index = 0
        self.update_selected()
        self.current_state = "default"
        minitel.cls()
        command_bar.set_state("dashboard-default")
        self.entities_updater.start()
        self.notification_monitor.start()  # Start notification monitoring
        self.display_registry.display()
        command_bar.display()
        while True:
            while self.buffer:
                char = self.buffer[0]
                self.buffer = self.buffer[1:]
                self.on_key(char)
            self.display_registry.update()
            command_bar.update()
            if self.should_stop:
                self.entities_updater.running = False
                self.notification_monitor.stop()  # Stop notification monitoring
                return
            time.sleep(0.1)

    @staticmethod
    def controller_from_entity(entity_id):
        if entity_id.startswith("light"):
            return LightController(entity_id)
        if entity_id.startswith("input_select"):
            return InputSelectController(entity_id)
        return EntityController(entity_id)

    def on_key(self, char):
        self.state_actions[self.current_state](char)

    def default(self, char):
        if char == SpecialCharacters.ARROW_DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.controllers)
            self.update_selected()
        if char == SpecialCharacters.ARROW_UP:
            self.selected_index = (self.selected_index - 1) % len(self.controllers)
            self.update_selected()
        if char == SpecialCharacters.SUMMARY:
            self.current_state = "navigation"
            command_bar.set_state("navigation")
        elif char == SpecialCharacters.ENTER:
            self.controllers[self.selected_index].trigger()

    def navigation(self, char):
        if char == SpecialCharacters.ESCAPE:
            command_bar.set_state("dashboard-default")
        elif char == SpecialCharacters.ENTER:
            self.should_stop = True
            self.next_tab = "menu"