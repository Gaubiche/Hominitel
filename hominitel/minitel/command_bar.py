from hominitel.minitel.command_bar_state import CommandBarState
from hominitel.renderer.render_registry import RenderRegistry
from hominitel.renderer.template_element import TemplateElement


class CommandBar:
    def __init__(self):
        self.states = []
        self.current_state = None
        self.render_registry = RenderRegistry(top=23, bottom=25)
        self.render_registry.register(TemplateElement(self.content, True))

    def register(self, state):
        self.states.append(state)

    def set_state(self, state_string):
        for state in self.states:
            if state.name == state_string:
                self.current_state = state
                self.render_registry.update()
                return
        raise ValueError(f"State {state_string} not found in command bar states.")

    def content(self):
        return self.current_state.content if self.current_state else ""

    def display(self):
        self.render_registry.display()

    def update(self):
        self.render_registry.update()

command_bar = CommandBar()
command_bar.register(CommandBarState("dashboard-default", "↑↓: Browse, Enter: Toggle"))
command_bar.register(CommandBarState("navigation", "Enter: Go to menu, Esc: Back"))
command_bar.register(CommandBarState("menu-default", "↑↓: Browse, Enter: Open tab"))
command_bar.register(CommandBarState("prompt-default", "> "))