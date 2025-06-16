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
        self.display_registry.register(TemplateElement(self.get_input, True))
        self.display_registry.register(TemplateElement(self.get_response, True))

    def get_input(self):
        return "> " + self.input

    def get_response(self):
        return " " * 6 + self.response

    def run(self):
        self.should_stop = False
        self.current_state = "default"
        minitel.cls()
        command_bar.set_state("prompt-default")
        while True:
            while self.buffer:
                char = self.buffer[0]
                self.buffer = self.buffer[1:]
                self.on_key(char)
            self.display_registry.update()
            if self.should_stop:
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
        elif char == SpecialCharacters.ENTER:
            self.should_stop = True
            self.next_tab = "menu"
