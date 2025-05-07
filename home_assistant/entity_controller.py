from controller.select import Selectable
from home_assistant.entity import Entity


class EntityController(Selectable, Entity):
    def __init__(self, minitel, entity_id):
        Entity.__init__(self, entity_id)
        super().__init__(minitel, self.content)

    def content(self):
        return f"{self.name} - {self.get_state_string()}"
