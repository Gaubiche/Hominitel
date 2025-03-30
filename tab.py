class Tab:
    def __init__(self, minitel, description=""):
        self.minitel = minitel
        self.description = description
        self.buffer = ""
        self.should_stop = False

    def run(self):
        pass

    def add_to_buffer(self, key):
        self.buffer += key

    def terminate(self):
        self.should_stop = True