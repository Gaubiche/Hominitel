class Tab:
    """
    This class represents a tab in the Minitel interface.
    Each tab has a description and a buffer for keyboard input, the buffer is filled by the tab handler.
    The run method is called in a loop until the tab is terminated.
    The tab is responsible for returning when should_stop is set to True.
    """
    def __init__(self, description=""):
        self.description = description
        self.buffer = ""
        self.should_stop = False

    def run(self):
        pass

    def add_to_buffer(self, key):
        self.buffer += key

    def terminate(self):
        self.should_stop = True