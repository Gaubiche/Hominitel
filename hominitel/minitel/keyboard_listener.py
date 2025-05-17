import _thread
import time

from hominitel.minitel.special_characters import SpecialCharacters

class KeyboardListener:
    def __init__(self, display_controller):
        self.running = True
        self.display_controller = display_controller

    def listen(self):
        from hominitel.minitel.minitel import minitel
        while self.running:
            last_char = minitel.get_input()
            if last_char is not None:
                self.display_controller.on_keys(self.split_input(last_char))
            time.sleep(0.1)

    def start(self):
        _thread.start_new_thread(self.listen, ())

    def stop(self):
        self.running = False

    @staticmethod
    def split_input(input_str):
        i = 0
        res = []
        while i < len(input_str):
            for special_char in SpecialCharacters.list:
                if input_str[i:].startswith(special_char):
                    res.append(special_char)
                    i += len(special_char)
                    break
            res.append(input_str[i])
            i += 1
        return res

