from hominitel.controller.selectable import Selectable
from hominitel.home_assistant.light import Light


class LightController(Selectable, Light):
    def __init__(self, entity_id):
        Light.__init__(self, entity_id)
        super().__init__(self.content)

    def content(self):
        return f"{self.name} - {self.get_state_string()}"

    def trigger(self):
        self.toggle()
