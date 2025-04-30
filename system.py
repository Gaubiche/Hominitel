from machine import UART

from tab_handler import TabHandler
from lib import upynitel


class System:
    def __init__(self):
        self.minitel = upynitel.Pynitel(UART(2, baudrate=1200, parity=0, bits=7, stop=1))
        self.minitel.echo_off()
        self.minitel.cls()
        self.line = 4
        self.application_handler = TabHandler(self.minitel)

    def print(self, message: str):
        self.minitel.vtab(self.line)
        self.minitel._print("> " + message)
        self.line += 2

    def run(self):
        self.application_handler.run()
