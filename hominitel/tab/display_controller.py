import _thread

from hominitel.minitel.command_bar_state import CommandBarState
from hominitel.tab.tab import Tab
from hominitel.tab.tabs.menu import Menu
from hominitel.minitel.keyboard_listener import KeyboardListener
from hominitel.tab.tabs.dashboard import Dashboard
from hominitel.tab.tabs.prompt import Prompt
from hominitel.tab.tabs.config import ConfigTab
from hominitel.minitel.special_characters import SpecialCharacters


class DisplayController:
    """
    This class handles the active tab and passes the keyboard buffer.
    It is responsible for switching between tabs and managing the keyboard listener.
    It also handles the registration of tabs, the default tab and the key bindings for each tab.
    """
    def __init__(self):
        self.tabs = {}
        self.current_tab = None
        self.default_tab = None
        self.register_tab(Dashboard(), 'dashboard', True)
        self.register_tab(Prompt(), 'prompt')
        self.register_tab(ConfigTab(), 'config')
        self.register_tab(Menu(self.tabs), 'menu')
        self.keyboard_listener = KeyboardListener(self)

    def register_tab(self, tab: Tab, name, default=False):
        self.tabs[name] = tab
        if default:
            self.default_tab = tab

    def is_tab_launch_key(self, key):
        return key in self.tabs.keys()

    def open_tab_from_name(self, name):
        tab = self.tabs[name]
        self.open_tab(tab)

    def open_tab(self, tab):
        if self.current_tab and tab!=self.current_tab:
            self.current_tab.terminate()
        self.current_tab = tab
        self.current_tab.should_stop = False

    def on_keys(self, value):
        self.current_tab.buffer += value

    def run(self):
        _thread.start_new_thread(self.keyboard_listener.listen, ())
        self.open_tab(self.default_tab)
        while True:
            self.current_tab.run()
            self.open_tab_from_name(self.current_tab.next_tab)
