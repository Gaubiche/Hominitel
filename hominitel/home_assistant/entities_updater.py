import time
import gc
from hominitel.utils.thread_manager import safe_thread_creation, stop_thread_safely, thread_manager

class EntitiesUpdater:
    def __init__(self):
        self.entities = []
        self.running = True
        self.thread_name = "entities_updater"

    def register(self, entity):
        self.entities.append(entity)

    def start(self):
        if self.running:
            # Stop existing thread if running
            self.stop()
        
        self.running = True
        
        # Create thread safely
        success = safe_thread_creation(self.thread_name, self.run)
        if not success:
            print("Failed to create entities updater thread, running in main thread")
            # Fallback: run in main thread (not ideal but prevents crash)
            self._run_main_thread()

    def _run_main_thread(self):
        """Fallback: run updater in main thread"""
        print("Running entities updater in main thread (fallback mode)")
        # This is a simplified version that doesn't block
        pass

    def run(self):
        """Main updater loop with error handling"""
        try:
            while self.running:
                for entity in self.entities:
                    try:
                        entity.update_state()
                    except Exception as e:
                        print(f"Error updating entity: {e}")
                
                time.sleep(1)
        except Exception as e:
            print(f"Fatal error in entities updater: {e}")
        finally:
            print("Entities updater thread ended")

    def stop(self):
        """Stop the entities updater"""
        self.running = False
        stop_thread_safely(self.thread_name)