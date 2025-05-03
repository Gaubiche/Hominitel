from api.minitel_client import MinitelClient
from lib.upynitel import Pynitel

class PynitelClient(Pynitel, MinitelClient):
    def _if(self):
        last_char = self.minitel._if()
        if last_char is None:
            return None
        if isinstance(last_char, bytes):
            return last_char.decode('utf-8')
        return last_char
