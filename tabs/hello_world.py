import time

from tab import Tab


class HelloWorld(Tab):
    def __init__(self, minitel):
        super().__init__(minitel, description="Displays a 'Hello world'")

    def run(self):
        self.minitel.cls()
        self.minitel.vtab(4)
        self.minitel._print("Hello, World!")
        while True:
            if self.should_stop:
                return
            time.sleep(0.1)