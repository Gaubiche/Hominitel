# from machine import UART
from api.simu_client import MinitelSimuClient
from tab_handler import TabHandler
import curses

class System:
    def __init__(self):
        self.minitel = MinitelSimuClient()
        self.minitel.echo_off()
        self.minitel.cls()
        self.line = 4
        self.application_handler = TabHandler(self.minitel)

    def run(self):
        self.application_handler.run()
