from home_assistant.home_assistant import HomeAssistantAPI

class Entity:
    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.api = HomeAssistantAPI()
        self.is_settable = False
        print(self.get_state())
        self.name = self.get_state()["attributes"]["friendly_name"]
        self.is_on = False

    def get_state(self):
        return self.api.get_state(self.entity_id)

    def get_state_string(self):
        return self.get_state()["state"]

    def get_boolean_state(self):
        return False

    def set_state(self, state):
        pass