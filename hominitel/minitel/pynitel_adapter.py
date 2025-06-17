from hominitel.minitel.adapter import Adapter
from hominitel.minitel.lib.upynitel import Pynitel

class PynitelAdapter(Pynitel, Adapter):
    def print(self, text: str):
        self._print(text)

    def get_input(self):
        last_char = self._if()
        if last_char is None or last_char == b'\x1b;cZD':
            return None
        if isinstance(last_char, bytes):
            return last_char.decode('utf-8')
        return last_char

    def message(self, row: int, col: int, delay: int, message: str, bip: bool = False):
        super().message(row, col, delay, message, bip)
