from hominitel.tab.display_controller import DisplayController
from hominitel.minitel.minitel import minitel
from hominitel.home_assistant.notification_monitor import NotificationMonitor

class System:
    """
    This class is the main entry point for the Minitel (or emulator) system.
    It initializes the Minitel interface and the tab handler.
    """
    def __init__(self):
        minitel.echo_off()
        minitel.cls()
        self.line = 4
        self.application_handler = DisplayController()

    def run(self):
        try:
            self.application_handler.run()
        except KeyboardInterrupt:
            print("Shutting down...")
        finally:
            # Clean up notification monitor
            notification_monitor = NotificationMonitor()
            notification_monitor.stop()
            print("Notification monitor stopped.")
