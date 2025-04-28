from home_assistant.entity import Entity

class Light(Entity):
    def __init__(self, entity_id):
        super().__init__(entity_id)
        self.is_on = False

    def get_state_string(self):
        return "On" if self.get_state()["state"] == "on" else "Off"

    def get_state(self):
        state = super().get_state()
        if state["state"] == "on":
            self.is_on = True
        else:
            self.is_on = False
        return state

    def set_state(self, state):
        if state == "on":
            self.api.set_state(self.entity_id, "light", "turn_on")
        elif state == "off":
            self.api.set_state(self.entity_id, "light", "turn_off")
        else:
            raise ValueError("Invalid state. Use 'on' or 'off'.")

    def get_boolean_state(self):
        return self.is_on