try:
    from machine import UART # only accessible on ESP32
    from hominitel.minitel.pynitel_adapter import PynitelAdapter
    ON_MINITEL = True
except:
    from hominitel.minitel.emulator_adapter import SimuAdapter
    import curses
    ON_MINITEL = False


from hominitel.tab.tab_handler import TabHandler

class System:
    """
    This class is the main entry point for the Minitel (or emulator) system.
    It initializes the Minitel interface and the tab handler.
    """
    def __init__(self):
        if ON_MINITEL:
            self.minitel = PynitelAdapter(UART(2, baudrate=1200, parity=0, bits=7, stop=1))
        else:    
            self.minitel = SimuAdapter()
        self.minitel.echo_off() # prevent typing on the screen
        self.minitel.cls()
        self.line = 4
        self.application_handler = TabHandler(self.minitel)

    def run(self):
        self.application_handler.run()
