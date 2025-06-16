import time
import json

from hominitel.minitel.minitel import minitel
from hominitel.minitel.special_characters import SpecialCharacters
from hominitel.renderer.render_registry import RenderRegistry
from hominitel.renderer.template_element import TemplateElement
from hominitel.tab.tab import Tab
from hominitel.minitel.command_bar import command_bar
from hominitel.config import config

class ConfigTab(Tab):
    def __init__(self):
        super().__init__(description="Dashboard Configuration")
        self.current_state = "default"
        self.state_actions = {
            "default": self.default,
            "navigation": self.navigation,
            "add_entity": self.add_entity,
            "remove_entity": self.remove_entity,
        }
        self.selected_index = 0
        self.display_registry = RenderRegistry()
        self.update_display()

    def update_display(self):
        self.display_registry = RenderRegistry()
        self.display_registry.register(TemplateElement("Dashboard Entities Configuration"))
        self.display_registry.register(TemplateElement(""))
        
        # Display current entities
        for i, entity in enumerate(config.DASHBOARD_TAB["entities"]):
            prefix = "→ " if i == self.selected_index else "  "
            self.display_registry.register(TemplateElement(f"{prefix}{entity}"))

    def save_config(self):
        config.save()

    def run(self):
        self.should_stop = False
        self.current_state = "default"
        minitel.cls()
        command_bar.set_state("config-default")
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
        self.state_actions[self.current_state](char)

    def default(self, char):
        if char == SpecialCharacters.ARROW_DOWN:
            self.selected_index = (self.selected_index + 1) % len(config.DASHBOARD_TAB["entities"])
            self.update_display()
        elif char == SpecialCharacters.ARROW_UP:
            self.selected_index = (self.selected_index - 1) % len(config.DASHBOARD_TAB["entities"])
            self.update_display()
        elif char == SpecialCharacters.SUMMARY:
            self.current_state = "navigation"
            command_bar.set_state("config-navigation")
        elif char == SpecialCharacters.ENTER:
            self.current_state = "remove_entity"
            command_bar.set_state("config-remove")
        elif char == SpecialCharacters.SEND:
            self.current_state = "add_entity"
            command_bar.set_state("config-add")

    def navigation(self, char):
        if char == SpecialCharacters.ESCAPE:
            self.current_state = "default"
            command_bar.set_state("config-default")
        elif char == SpecialCharacters.ENTER:
            self.should_stop = True
            self.next_tab = "menu"

    def add_entity(self, char):
        if char == SpecialCharacters.ENTER:
            # Add the new entity
            new_entity = "".join(self.buffer).strip()
            if new_entity and new_entity not in config.DASHBOARD_TAB["entities"]:
                config.DASHBOARD_TAB["entities"].append(new_entity)
                self.save_config()
            self.buffer = []
            self.current_state = "default"
            command_bar.set_state("config-default")
            self.update_display()
        elif char == SpecialCharacters.ESCAPE:
            self.buffer = []
            self.current_state = "default"
            command_bar.set_state("config-default")
        elif char not in [SpecialCharacters.ARROW_UP, SpecialCharacters.ARROW_DOWN, 
                         SpecialCharacters.ARROW_LEFT, SpecialCharacters.ARROW_RIGHT]:
            self.buffer.append(char)

    def remove_entity(self, char):
        if char == SpecialCharacters.ENTER:
            # Remove the selected entity
            if config.DASHBOARD_TAB["entities"]:
                config.DASHBOARD_TAB["entities"].pop(self.selected_index)
                self.selected_index = min(self.selected_index, len(config.DASHBOARD_TAB["entities"]) - 1)
                self.save_config()
            self.current_state = "default"
            command_bar.set_state("config-default")
            self.update_display()
        elif char == SpecialCharacters.ESCAPE:
            self.current_state = "default"
            command_bar.set_state("config-default") 