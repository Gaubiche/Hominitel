import time
import _thread

class EntitiesUpdater:
    def __init__(self):
        self.entities = []
        self.running = True

    def register(self, entity):
        self.entities.append(entity)

    def start(self):
        self.running = True
        _thread.start_new_thread(self.run, ())

    def run(self):
        while self.running:
            for entity in self.entities:
                entity.update_state()
            time.sleep(1)