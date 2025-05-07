from home_assistant.home_assistant import HomeAssistantAPI

class Entity:
    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.api = HomeAssistantAPI()
        Entity.update_state(self)
        self.name = self.state["attributes"]["friendly_name"]

    def update_state(self):
        self.state = self.api.get_state(self.entity_id)
        return self.state

    def get_state_string(self):
        return self.state["state"]

    def get_boolean_state(self):
        return False

    def set_state(self, state):
        pass