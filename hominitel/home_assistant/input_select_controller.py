from hominitel.controller.selectable import Selectable
from hominitel.home_assistant.input_select import InputSelect


class InputSelectController(Selectable, InputSelect):
    def __init__(self, minitel, entity_id):
        InputSelect.__init__(self, entity_id)
        super().__init__(minitel, self.content)

    def content(self):
        return f"{self.name} - {self.get_state_string()}"

    def trigger(self):
        self.toggle()