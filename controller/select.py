from display.template_element import TemplateElement

class Selectable():
    def __init__(self, minitel, content):
        self.is_selected = False
        self.template_element = TemplateElement(minitel, content, self.inverse)

    def select(self):
        self.is_selected = True

    def deselect(self):
        self.is_selected = False

    def inverse(self):
        # Logic to check if the element is selected
        return self.is_selected

    def trigger(self):
        pass

    def get_template_element(self):
        return self.template_element