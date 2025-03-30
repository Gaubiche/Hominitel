import time

from tab import Tab


class Menu(Tab):
    def __init__(self, minitel, tabs):
        super().__init__(minitel, description="Main menu")
        self.minitel = minitel
        self.tabs = tabs

    def run(self):
        self.minitel.cls()
        self.minitel.vtab(2)
        self.minitel._print("Main menu")
        self.minitel.vtab(4)
        for key, tab in self.tabs.items():
            self.minitel._print(f"{key}: {tab.description}\n")
        while True:
            if self.should_stop:
                return
            time.sleep(0.1)