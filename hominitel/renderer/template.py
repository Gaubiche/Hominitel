from hominitel.minitel.lib import upynitel

from machine import UART

class Template:
    title_height = 1
    command_height = 1
    
    def __init__(self, title, helper):
        self.minitel = upynitel.Pynitel(UART(2, baudrate=1200, parity=0, bits=7, stop=1))
        assert len(title)<=40, "title should be less than 40 characters long"
        self.title = title
        assert len(helper)<=40, "title helper be less than 40 characters long"
        self.helper = helper
        
    def show_title(self):
        self.minitel.vtab(0)
        self.minitel.inverse()
        self.minitel.print(self.title)
    
    def show_helper(self):
        self.minitel.vtab(24)
        self.minitel.inverse()
        self.minitel.print(self.helper)
    
    def show(self):
        self.show_title()
        self.show_helper()
