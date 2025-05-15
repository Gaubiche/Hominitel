import _thread
import time

class KeyboardListener:
    def __init__(self, display_controller):
        self.running = True
        self.display_controller = display_controller

    def listen(self):
        from hominitel.minitel.minitel import minitel
        while self.running:
            last_char = minitel.get_input()
            if last_char is not None:
                self.display_controller.on_key(last_char)
            time.sleep(0.1)

    def start(self):
        _thread.start_new_thread(self.listen, ())

    def stop(self):
        self.running = False
