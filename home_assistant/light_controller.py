from controller.select import Selectable
from home_assistant.light import Light


class LightController(Selectable):
    def __init__(self, minitel, entity_id):
        self.light = Light(entity_id)
        super().__init__(minitel, self.content)

    def content(self):
        return f"{self.light.name} - {self.light.get_state_string()}"

    def trigger(self):
        self.light.toggle()