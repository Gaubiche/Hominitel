import _thread

from tab import Tab
from tabs.hello_world import HelloWorld
from tabs.menu import Menu
from keyboard_listener import KeyboardListener
from tabs.dashboard import Dashboard

class TabHandler:
    def __init__(self, minitel):
        self.tabs = {}
        self.current_tab = None
        self.register_tab(HelloWorld(minitel), 'H')
        self.register_tab(Dashboard(minitel), 'D')
        self.register_tab(Menu(minitel, self.tabs), 'M', True)
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
            print("Tab terminated")
        self.current_tab = tab
        self.current_tab.should_stop = False

    def send_to_buffer(self, value):
        self.current_tab.buffer += value

    def run(self):
        _thread.start_new_thread(self.keyboard_listener.listen, ())
        self.open_tab(self.default_tab)
        while True:
            self.current_tab.run()
