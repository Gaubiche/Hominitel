from hominitel.home_assistant.entity import Entity


class InputSelect(Entity):
    def __init__(self, entity_id):
        super().__init__(entity_id)
        
        # Initialize with safe defaults
        self.options = []
        self.current_option = "unknown"
        self.target_option = "unknown"
        
        # Try to get options safely
        try:
            if "attributes" in self.state and "options" in self.state["attributes"]:
                self.options = self.state["attributes"]["options"]
            else:
                self.options = ["unknown"]
                
            if "state" in self.state:
                self.current_option = self.state["state"]
                self.target_option = self.state["state"]
            else:
                self.current_option = "unknown"
                self.target_option = "unknown"
                
        except Exception as e:
            print(f"Error initializing InputSelect {entity_id}: {e}")
            # Use safe defaults
            self.options = ["unknown"]
            self.current_option = "unknown"
            self.target_option = "unknown"

    def update_state(self):
        """Update state with error handling"""
        try:
            super().update_state()
            
            # Update options safely
            if "attributes" in self.state and "options" in self.state["attributes"]:
                self.options = self.state["attributes"]["options"]
            
            # Update current option safely
            if "state" in self.state:
                new_state = self.state["state"]
                if self.current_option == self.target_option and new_state != self.current_option:
                    self.current_option = self.target_option = new_state
                self.current_option = new_state
                
        except Exception as e:
            print(f"Error updating InputSelect state: {e}")

    def get_state_string(self):
        """Get state string safely"""
        try:
            return self.current_option
        except Exception:
            return "unknown"

    def set_state(self, option):
        """Set state with error handling"""
        try:
            if option not in self.options:
                raise ValueError(f"Invalid option, not in entity's detected options: {self.options}")
            
            self.api.set_state(self.entity_id, "input_select", "select_option", {"option": option})
            
            # Update local state
            self.target_option = option
            
        except Exception as e:
            print(f"Error setting InputSelect state: {e}")
            raise

    def toggle(self):
        """Toggle option with error handling"""
        try:
            if not self.options or len(self.options) == 0:
                print("No options available for InputSelect")
                return
                
            current_index = 0
            if self.target_option in self.options:
                current_index = self.options.index(self.target_option)
            
            next_index = (current_index + 1) % len(self.options)
            self.target_option = self.options[next_index]
            self.set_state(self.target_option)
            
        except Exception as e:
            print(f"Error toggling InputSelect: {e}")
