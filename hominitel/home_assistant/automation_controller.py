from hominitel.controller.selectable import Selectable
from hominitel.home_assistant.automation import Automation


class AutomationController(Selectable, Automation):
    def __init__(self, entity_id):
        Automation.__init__(self, entity_id)
        super().__init__(self.content)

    def content(self):
        return f"{self.name} - {self.get_state_string()}"

    def trigger(self):
        self.toggle()