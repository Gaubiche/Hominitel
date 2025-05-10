from hominitel.minitel.adapter import Adapter
from hominitel.minitel.lib.upynitel import Pynitel

class PynitelAdapter(Pynitel, Adapter):
    def _if(self):
        last_char = self.minitel._if()
        if last_char is None:
            return None
        if isinstance(last_char, bytes):
            return last_char.decode('utf-8')
        return last_char
