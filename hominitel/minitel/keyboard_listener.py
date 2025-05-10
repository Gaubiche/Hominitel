import _thread
import time

from hominitel.minitel.minitel import minitel

class KeyboardListener:
    def __init__(self, application_handler):
        self.running = True
        self.application_handler = application_handler

    def listen(self):
        while self.running:
            last_char = minitel._if()
            if last_char is not None:
                if self.application_handler.is_tab_launch_key(last_char):
                    self.application_handler.open_tab_from_key(last_char)
                else:
                    self.application_handler.send_to_buffer(last_char)
            time.sleep(0.1)

    def start(self):
        _thread.start_new_thread(self.listen, ())

    def stop(self):
        self.running = False
