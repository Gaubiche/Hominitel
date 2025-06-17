import time
import json

from hominitel.minitel.minitel import minitel
from hominitel.minitel.special_characters import SpecialCharacters
from hominitel.renderer.render_registry import RenderRegistry
from hominitel.renderer.template_element import TemplateElement
from hominitel.tab.tab import Tab
from hominitel.minitel.command_bar import command_bar
from hominitel.config import config
from hominitel.controller.selectable import Selectable


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
        self.display_registry = RenderRegistry()
        self.template_elements = []
        self.controllers = []
        self.selected_index = 0
        self.init_display()

    def init_display(self):
        self.display_registry = RenderRegistry()
        self.template_elements = []
        self.controllers = []
        
        # Title
        title = TemplateElement("Dashboard Entities Configuration")
        self.display_registry.register(title)
        self.template_elements.append(title)
        
        # Empty line
        empty_line = TemplateElement("")
        self.display_registry.register(empty_line)
        self.template_elements.append(empty_line)
        
        # Entity lines
        for entity in config.DASHBOARD_TAB["entities"]:
            controller = Selectable(entity)
            self.display_registry.register(controller.get_template_element())
            self.controllers.append(controller)
            self.template_elements.append(controller.get_template_element())
        
        self.update_selected()

    def update_selected(self):
        for i, controller in enumerate(self.controllers):
            if i == self.selected_index:
                controller.select()
            else:
                controller.deselect()

    def update_display(self):
        # Clear the display registry
        self.display_registry.elements.clear()
        
        # Clear controllers and template elements
        self.controllers.clear()
        self.template_elements.clear()
        
        # Re-add title
        title = TemplateElement("Dashboard Entities Configuration")
        self.display_registry.register(title)
        self.template_elements.append(title)
        
        # Re-add empty line
        empty_line = TemplateElement("")
        self.display_registry.register(empty_line)
        self.template_elements.append(empty_line)
        
        # Recreate controllers in the new order
        for entity in config.DASHBOARD_TAB["entities"]:
            controller = Selectable(entity)
            self.display_registry.register(controller.get_template_element())
            self.controllers.append(controller)
            self.template_elements.append(controller.get_template_element())
        
        # Ensure selected_index is valid
        if self.controllers:
            self.selected_index = min(self.selected_index, len(self.controllers) - 1)
        else:
            self.selected_index = 0
            
        self.update_selected()

    def save_config(self):
        config.save()

    def move_selected_up(self):
        if self.selected_index > 0:
            config.DASHBOARD_TAB["entities"][self.selected_index], config.DASHBOARD_TAB["entities"][self.selected_index - 1] = config.DASHBOARD_TAB["entities"][self.selected_index - 1], config.DASHBOARD_TAB["entities"][self.selected_index]
            self.selected_index -= 1
            self.save_config()
            self.update_display()

    def move_selected_down(self):
        if self.selected_index < len(config.DASHBOARD_TAB["entities"]) - 1:
            config.DASHBOARD_TAB["entities"][self.selected_index], config.DASHBOARD_TAB["entities"][self.selected_index + 1] = config.DASHBOARD_TAB["entities"][self.selected_index + 1], config.DASHBOARD_TAB["entities"][self.selected_index]
            self.selected_index += 1
            self.save_config()
            self.update_display()

    def run(self):
        self.should_stop = False
        self.current_state = "default"
        self.selected_index = 0
        
        # Reinitialize display when tab is started
        self.init_display()
        
        minitel.cls()
        command_bar.set_state("config-default")
        self.display_registry.display()  # Initial display
        
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
            self.selected_index = (self.selected_index + 1) % len(self.controllers)
            self.update_selected()
        elif char == SpecialCharacters.ARROW_UP:
            self.selected_index = (self.selected_index - 1) % len(self.controllers)
            self.update_selected()
        elif char == SpecialCharacters.SUMMARY:
            self.current_state = "navigation"
            command_bar.set_state("config-navigation")
        elif char == SpecialCharacters.ENTER:
            self.current_state = "remove_entity"
            command_bar.set_state("config-remove")
        elif char == SpecialCharacters.SEND:
            self.current_state = "add_entity"
            command_bar.set_state("config-add")
        elif char == SpecialCharacters.BACK:
            self.move_selected_up()
        elif char == SpecialCharacters.REPEAT:
            self.move_selected_down()

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
            if config.DASHBOARD_TAB["entities"] and self.selected_index < len(config.DASHBOARD_TAB["entities"]):
                config.DASHBOARD_TAB["entities"].pop(self.selected_index)
                self.save_config()
                self.current_state = "default"
                command_bar.set_state("config-default")
                
                # Adjust selected_index if needed
                if config.DASHBOARD_TAB["entities"]:
                    self.selected_index = min(self.selected_index, len(config.DASHBOARD_TAB["entities"]) - 1)
                else:
                    self.selected_index = 0
                    
                self.update_display()
        elif char == SpecialCharacters.ESCAPE:
            self.current_state = "default"
            command_bar.set_state("config-default") 