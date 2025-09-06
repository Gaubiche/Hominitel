import time
from hominitel.home_assistant.entity import Entity
from hominitel.minitel.minitel import minitel
from hominitel.config import config
from hominitel.utils.thread_manager import safe_thread_creation, stop_thread_safely

class NotificationMonitor:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NotificationMonitor, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.notification_entity = None
            self.last_notification_value = None
            self.running = True
            self.thread_name = "notification_monitor"
            self._initialized = True

    def start(self):
        """Starts monitoring the configured notification entity"""
        # Only start if not already running
        if self.running and self.notification_entity is None:
            try:
                # Use the configured entity or a default value
                notification_entity_id = getattr(config, 'NOTIFICATION_ENTITY', 'input_text.notification')
                
                if notification_entity_id:
                    self.notification_entity = Entity(notification_entity_id)
                    self.last_notification_value = self.notification_entity.get_state_string()
                    self.running = True
                    
                    # Create thread safely
                    success = safe_thread_creation(self.thread_name, self.run)
                    if success:
                        print(f"Notification monitoring activated for entity: {notification_entity_id}")
                    else:
                        print("Failed to create notification monitor thread")
                        self.running = False
                else:
                    print("No notification entity configured")
                    
            except Exception as e:
                print(f"Error initializing notification monitoring: {e}")
                self.running = False

    def run(self):
        """Main loop for monitoring notifications with error handling"""
        try:
            while self.running:
                try:
                    if self.notification_entity:
                        self.notification_entity.update_state()
                        current_value = self.notification_entity.get_state_string()
                        
                        # Check if the value has changed and is not empty
                        if (self.last_notification_value is not None and 
                            current_value != self.last_notification_value and 
                            current_value.strip() != ""):
                            
                            # Display a notification with sound beep
                            minitel.message(20, 1, 3, f"NOTIFICATION: {current_value}", True)
                        
                        self.last_notification_value = current_value
                        
                except Exception as e:
                    print(f"Error during notification monitoring: {e}")
                    
                time.sleep(1)
                
        except Exception as e:
            print(f"Fatal error in notification monitor: {e}")
        finally:
            print("Notification monitor thread ended")

    def stop(self):
        """Stops notification monitoring"""
        self.running = False
        stop_thread_safely(self.thread_name)
        # Reset entity to allow restart if needed
        self.notification_entity = None
        self.last_notification_value = None 