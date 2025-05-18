from hominitel.renderer.render_registry import RenderRegistry
from hominitel.renderer.template_element import TemplateElement


class CommandBar:
    def __init__(self):
        self.states = []
        self.current_state = None
        self.default_state = None
        self.render_registry = RenderRegistry(top=23, bottom=25)
        self.render_registry.register(TemplateElement(self.content, True))

    def register(self, state, default=False):
        self.states.append(state)
        if self.current_state is None:
            self.current_state = state
        if default:
            self.current_state = state
            self.default_state = state

    def content(self):
        return self.current_state.content if self.current_state else ""

    def display(self):
        self.render_registry.display()

    def update(self):
        self.render_registry.update()
