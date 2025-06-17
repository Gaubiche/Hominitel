import time
import _thread
from hominitel.home_assistant.entity import Entity
from hominitel.minitel.minitel import minitel
from hominitel.config import config

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
                    _thread.start_new_thread(self.run, ())
                    print(f"Notification monitoring activated for entity: {notification_entity_id}")
                else:
                    print("No notification entity configured")
                    
            except Exception as e:
                print(f"Error initializing notification monitoring: {e}")

    def run(self):
        """Main loop for monitoring notifications"""
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

    def stop(self):
        """Stops notification monitoring"""
        self.running = False
        # Reset entity to allow restart if needed
        self.notification_entity = None
        self.last_notification_value = None 