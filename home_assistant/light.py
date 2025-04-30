from home_assistant.entity import Entity

class Light(Entity):
    def __init__(self, entity_id):
        super().__init__(entity_id)
        self.is_on = self.state["state"] == "on"

    def update_state(self):
        super().update_state()
        self.is_on = self.state["state"] == "on"

    def get_state_string(self):
        return "On" if self.is_on else "Off"

    def set_state(self, state):
        if state not in ["on", "off"]:
            raise ValueError("Invalid state. Use 'on' or 'off'.")
        self.api.set_state(self.entity_id, "light", f"turn_{state}")

    def toggle(self):
        if self.is_on:
            self.set_state("off")
        else:
            self.set_state("on")

    def get_boolean_state(self):
        return self.is_on