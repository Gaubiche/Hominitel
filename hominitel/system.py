from hominitel.tab.tab_handler import TabHandler
from hominitel.minitel.minitel import minitel

class System:
    """
    This class is the main entry point for the Minitel (or emulator) system.
    It initializes the Minitel interface and the tab handler.
    """
    def __init__(self):
        minitel.echo_off()
        minitel.cls()
        self.line = 4
        self.application_handler = TabHandler()

    def run(self):
        self.application_handler.run()
