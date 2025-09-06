import gc
from hominitel.tab.display_controller import DisplayController
from hominitel.minitel.minitel import minitel
from hominitel.home_assistant.notification_monitor import NotificationMonitor
from hominitel.utils.memory_manager import memory_manager, emergency_cleanup

class System:
    """
    This class is the main entry point for the Minitel (or emulator) system.
    It initializes the Minitel interface and the tab handler.
    """
    def __init__(self):
        # Initialize memory management
        memory_manager.force_cleanup()
        
        minitel.echo_off()
        minitel.cls()
        self.line = 4
        self.application_handler = DisplayController()

    def run(self):
        try:
            # Monitor memory before starting
            memory_manager.check_memory_pressure()
            
            self.application_handler.run()
        except MemoryError as e:
            print(f"Memory error in system: {e}")
            emergency_cleanup()
            print("System recovered from memory error")
        except KeyboardInterrupt:
            print("Shutting down...")
        except Exception as e:
            print(f"System error: {e}")
            emergency_cleanup()
        finally:
            # Clean up notification monitor
            try:
                notification_monitor = NotificationMonitor()
                notification_monitor.stop()
                print("Notification monitor stopped.")
            except Exception as e:
                print(f"Error stopping notification monitor: {e}")
            
            # Final cleanup
            memory_manager.force_cleanup()
            print("System cleanup completed")
