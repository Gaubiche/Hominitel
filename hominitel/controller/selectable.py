from hominitel.renderer.template_element import TemplateElement

class Selectable:
    def __init__(self, content):
        self.is_selected = False
        self.template_element = TemplateElement(content, lambda: self.get_selection_indicator())
        self.content = content

    def select(self):
        self.is_selected = True

    def deselect(self):
        self.is_selected = False

    def get_selection_indicator(self):
        """Returns a selection indicator (arrow) if selected, empty string otherwise"""
        return "→ " if self.is_selected else "  "

    def trigger(self):
        pass

    def get_template_element(self):
        return self.template_element