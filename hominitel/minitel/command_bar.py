from hominitel.minitel.command_bar_state import CommandBarState
from hominitel.renderer.render_registry import RenderRegistry
from hominitel.renderer.template_element import TemplateElement


class CommandBar:
    def __init__(self):
        self.states = []
        self.current_state = None
        self.dynamic_content_callback = None
        self.render_registry = RenderRegistry(top=23, bottom=25)
        self.render_registry.register(TemplateElement(self.content))

    def register(self, state):
        self.states.append(state)

    def set_state(self, state_string):
        for state in self.states:
            if state.name == state_string:
                self.current_state = state
                # Clear dynamic content when changing state
                self.dynamic_content_callback = None
                self.render_registry.update()
                return
        raise ValueError(f"State {state_string} not found in command bar states.")

    def set_dynamic_content(self, callback):
        """Set a callback function that returns dynamic content for the command bar"""
        self.dynamic_content_callback = callback
        self.render_registry.update()

    def clear_dynamic_content(self):
        """Clear the dynamic content and return to static state content"""
        self.dynamic_content_callback = None
        self.render_registry.update()

    def content(self):
        if self.dynamic_content_callback:
            return self.dynamic_content_callback()
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
command_bar.register(CommandBarState("prompt-navigation", "Enter: Go to menu, Esc: Back"))
command_bar.register(CommandBarState("config-default", "↑↓: Browse, Enter: Remove, Send: Add"))
command_bar.register(CommandBarState("config-navigation", "Enter: Go to menu, Esc: Back"))
command_bar.register(CommandBarState("config-add", "Enter: Add entity, Esc: Cancel"))
command_bar.register(CommandBarState("config-remove", "Enter: Remove entity, Esc: Cancel"))