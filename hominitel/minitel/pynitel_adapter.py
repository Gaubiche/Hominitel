from hominitel.minitel.adapter import Adapter
from hominitel.minitel.lib.upynitel import Pynitel

class PynitelAdapter(Pynitel, Adapter):
    def get_input(self):
        last_char = self._if()
        if last_char is None or last_char == b'\x1b;cZD':
            return None
        if isinstance(last_char, bytes):
            return last_char.decode('utf-8')
        return last_char
