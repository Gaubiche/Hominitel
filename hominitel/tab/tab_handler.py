import _thread

from hominitel.tab.tab import Tab
from hominitel.tab.tabs.hello_world import HelloWorld
from hominitel.tab.tabs.menu import Menu
from hominitel.minitel.keyboard_listener import KeyboardListener
from hominitel.tab.tabs.dashboard import Dashboard
from hominitel.tab.tabs.prompt import Prompt


class TabHandler:
    """
    This class handles the active tab and passes the keyboard buffer.
    It is responsible for switching between tabs and managing the keyboard listener.
    It also handles the registration of tabs, the default tab and the key bindings for each tab.
    """
    def __init__(self, minitel):
        self.tabs = {}
        self.current_tab = None
        self.register_tab(HelloWorld(minitel), 'H')
        self.register_tab(Dashboard(minitel), 'D', True)
        self.register_tab(Prompt(minitel), 'P')
        self.register_tab(Menu(minitel, self.tabs), 'M')
        self.keyboard_listener = KeyboardListener(self, minitel)

    def register_tab(self, tab: Tab, key, default=False):
        self.tabs[key] = tab
        if default:
            self.default_tab = tab

    def is_tab_launch_key(self, key):
        return key in self.tabs.keys()

    def open_tab_from_key(self, key):
        tab = self.tabs[key]
        self.open_tab(tab)

    def open_tab(self, tab):
        if self.current_tab and tab!=self.current_tab:
            self.current_tab.terminate()
        self.current_tab = tab
        self.current_tab.should_stop = False

    def send_to_buffer(self, value):
        self.current_tab.buffer += value

    def run(self):
        _thread.start_new_thread(self.keyboard_listener.listen, ())
        self.open_tab(self.default_tab)
        while True:
            self.current_tab.run()
