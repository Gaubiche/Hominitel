try:
    from machine import UART
    from api.upynitel_client import PynitelClient
    ON_MINITEL = True
except:
    from api.simu_client import MinitelSimuClient
    import curses
    ON_MINITEL = False


from tab_handler import TabHandler

class System:
    def __init__(self):
        if ON_MINITEL:
            self.minitel = PynitelClient(UART(2, baudrate=1200, parity=0, bits=7, stop=1))
        else:    
            self.minitel = MinitelSimuClient()
        self.minitel.echo_off()
        self.minitel.cls()
        self.line = 4
        self.application_handler = TabHandler(self.minitel)

    def run(self):
        self.application_handler.run()
