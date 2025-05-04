from controller.select import Selectable
from home_assistant.entity import Entity


class EntityController(Selectable):
    def __init__(self, minitel, entity_id):
        self.entity = Entity(entity_id)
        super().__init__(minitel, self.content)

    def get_entity(self):
        return self.entity

    def content(self):
        return f"{self.entity.name} - {self.entity.get_state_string()}"
