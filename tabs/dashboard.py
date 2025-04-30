import time

from display.display_registry import DisplayRegistry
from home_assistant.entities_updater import EntitiesUpdater
from home_assistant.light_controller import LightController
from tab import Tab

class Dashboard(Tab):
    def __init__(self, minitel):
        super().__init__(minitel, description="Home Assistant Dashboard")
        self.controllers = []
        self.controllers.append(LightController(minitel, "light.salon"))
        self.controllers.append(LightController(minitel, "light.ampoule_boudha_prise_1"))
        self.controllers.append(LightController(minitel, "light.lampe_bibliotheque_prise_1"))
        self.controllers.append(LightController(minitel, "light.osram_lightify_indoor_flex_rgbw_lumiere"))
        self.controllers.append(LightController(minitel, "light.divoom_pixoo_64_light"))
        self.selected_index = 0
        self.display_registry = DisplayRegistry(top=10, bottom=20)
        self.entities_updater = EntitiesUpdater()
        for controller in self.controllers:
            self.display_registry.register(controller.get_template_element())
            self.entities_updater.register(controller.get_entity())
        self.update_selected()

    def update_selected(self):
        for i, controller in enumerate(self.controllers):
            if i == self.selected_index:
                controller.select()
            else:
                controller.deselect()

    def run(self):
        self.minitel.cls()
        self.entities_updater.start()
        self.display_registry.display()
        while True:
            while self.buffer!= "":
                char = self.buffer[0]
                self.buffer = self.buffer[1:]
                if char == " ":
                    self.selected_index = (self.selected_index + 1) % len(self.controllers)
                    self.update_selected()
                elif char == "\r":
                    self.controllers[self.selected_index].trigger()
            self.display_registry.update()
            if self.should_stop:
                self.entities_updater.running = False
                return
            time.sleep(0.1)
