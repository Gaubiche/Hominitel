import time

from hominitel.home_assistant.home_assistant import home_assistant_api
from hominitel.minitel.command_bar import command_bar
from hominitel.minitel.minitel import minitel
from hominitel.minitel.special_characters import SpecialCharacters, SPECIAL_CHARACTER_LIST
from hominitel.renderer.render_registry import RenderRegistry
from hominitel.renderer.template_element import TemplateElement
from hominitel.tab.tab import Tab


class Prompt(Tab):
    def __init__(self):
        super().__init__(description="Prompt Mode for Home Assistant")
        self.current_state = "default"
        self.state_actions = {
            "default": self.default,
            "navigation": self.navigation,
        }
        self.input = ""
        self.response = ""
        self.display_registry = RenderRegistry()
        # Only register the response element, input will be in command bar
        self.display_registry.register(TemplateElement(self.get_response))

    def get_input(self):
        return "> " + self.input

    def get_response(self):
        return self.response

    def run(self):
        self.should_stop = False
        self.current_state = "default"
        minitel.cls()
        command_bar.set_state("prompt-default")
        # Set dynamic content for input in command bar
        command_bar.set_dynamic_content(self.get_input)
        while True:
            while self.buffer:
                char = self.buffer[0]
                self.buffer = self.buffer[1:]
                self.on_key(char)
            self.display_registry.update()
            command_bar.update()  # Update command bar to show input changes
            if self.should_stop:
                # Clear dynamic content when leaving the tab
                command_bar.clear_dynamic_content()
                return

    def on_key(self, char):
        self.state_actions[self.current_state](char)

    def default(self, char):
        if char == SpecialCharacters.ENTER:
            self.response = home_assistant_api.prompt(self.input)
            self.input = ""
            return
        if char == SpecialCharacters.ARROW_LEFT:
            if self.input:
                self.input = self.input[:-1]
            return
        if char == SpecialCharacters.SUMMARY:
            self.current_state = "navigation"
            command_bar.set_state("prompt-navigation")
            return
        if char in SPECIAL_CHARACTER_LIST:
            return
        self.input += char

    def navigation(self, char):
        if char == SpecialCharacters.ESCAPE:
            self.current_state = "default"
            command_bar.set_state("prompt-default")
            # Restore dynamic content for input
            command_bar.set_dynamic_content(self.get_input)
        elif char == SpecialCharacters.ENTER:
            self.should_stop = True
            self.next_tab = "menu"
