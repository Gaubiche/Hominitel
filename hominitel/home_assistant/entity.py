from hominitel.home_assistant.home_assistant import HomeAssistantAPI

class Entity:
    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.api = HomeAssistantAPI()
        
        # Initialize with safe defaults
        self.state = {
            "entity_id": entity_id,
            "state": "unknown",
            "attributes": {"friendly_name": entity_id.split('.')[1]}
        }
        
        # Update state with error handling
        try:
            self.update_state()
        except Exception as e:
            print(f"Error initializing entity {entity_id}: {e}")
        
        # Extract name safely
        try:
            self.name = self.state["attributes"]["friendly_name"] if "friendly_name" in self.state["attributes"] else self.state["entity_id"].split('.')[1]
        except (KeyError, TypeError):
            self.name = entity_id.split('.')[1]

    def update_state(self):
        """Update entity state with memory management"""
        try:
            self.state = self.api.get_state(self.entity_id)
            return self.state
            
        except MemoryError as e:
            print(f"Memory error updating state for {self.entity_id}: {e}")
            # Keep current state or use minimal fallback
            if not hasattr(self, 'state') or not self.state:
                self.state = {
                    "entity_id": self.entity_id,
                    "state": "unknown",
                    "attributes": {"friendly_name": self.entity_id.split('.')[1]}
                }
            return self.state
        except Exception as e:
            print(f"Error updating state for {self.entity_id}: {e}")
            raise

    def get_state_string(self):
        """Get state string safely"""
        try:
            return self.state["state"]
        except (KeyError, TypeError):
            return "unknown"

    def get_boolean_state(self):
        return False

    def set_state(self, state):
        """Set state with memory management"""
        pass