from home_assistant.entity import Entity


class InputSelect(Entity):
    def __init__(self, entity_id):
        super().__init__(entity_id)
        self.options = self.state["attributes"]["options"]
        self.current_option = self.state["state"]
        self.target_option = self.state["state"]

    def update_state(self):
        super().update_state()
        if self.current_option == self.target_option and self.state["state"] != self.current_option:
            self.current_option = self.target_option = self.state["state"]
        self.current_option = self.state["state"]

    def get_state_string(self):
        return self.current_option

    def set_state(self, option):
        if option not in self.options:
            raise ValueError(f"Invalid option, not in entity's detected options: {self.options}")
        self.api.set_state(self.entity_id, "input_select", "select_option", {"option": option})

    def toggle(self):
        self.target_option = self.options[(self.options.index(self.target_option) + 1)%len(self.options)]
        self.set_state(self.target_option)
