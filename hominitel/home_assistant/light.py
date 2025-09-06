from hominitel.home_assistant.entity import Entity

class Light(Entity):
    def __init__(self, entity_id):
        super().__init__(entity_id)
        
        # Initialize with safe default
        self.is_on = False
        
        # Update state safely
        try:
            self.is_on = self.state["state"] == "on"
        except (KeyError, TypeError):
            self.is_on = False

    def update_state(self):
        """Update light state with memory management"""
        try:
            super().update_state()
            self.is_on = self.state["state"] == "on"
        except Exception as e:
            print(f"Error updating light state: {e}")
            raise

    def get_state_string(self):
        """Get state string safely"""
        try:
            return "On" if self.is_on else "Off"
        except Exception:
            return "Unknown"

    def set_state(self, state):
        """Set light state with memory management"""
        if state not in ["on", "off"]:
            raise ValueError("Invalid state. Use 'on' or 'off'.")
        
        try:
            self.api.set_state(self.entity_id, "light", f"turn_{state}")
            
            # Update local state
            self.is_on = state == "on"
        except Exception as e:
            print(f"Error setting light state: {e}")
            raise

    def toggle(self):
        """Toggle light state with memory management"""
        try:
            if self.is_on:
                self.set_state("off")
            else:
                self.set_state("on")
        except Exception as e:
            print(f"Error toggling light: {e}")
            raise

    def get_boolean_state(self):
        """Get boolean state safely"""
        try:
            return self.is_on
        except Exception:
            return False