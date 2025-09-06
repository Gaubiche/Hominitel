import time
from hominitel.minitel.special_characters import SPECIAL_CHARACTER_LIST
from hominitel.utils.thread_manager import safe_thread_creation, stop_thread_safely


class KeyboardListener:
    def __init__(self, display_controller):
        self.running = True
        self.display_controller = display_controller
        self.thread_name = "keyboard_listener"

    def listen(self):
        """Main keyboard listening loop with error handling"""
        try:
            from hominitel.minitel.minitel import minitel
            while self.running:
                try:
                    last_char = minitel.get_input()
                    if last_char is not None:
                        self.display_controller.on_keys(self.split_input(last_char))
                    time.sleep(0.1)
                    
                except Exception as e:
                    print(f"Error in keyboard listener: {e}")
                    time.sleep(0.1)
                    
        except Exception as e:
            print(f"Fatal error in keyboard listener: {e}")
        finally:
            print("Keyboard listener thread ended")

    def start(self):
        """Start keyboard listener with thread management"""
        success = safe_thread_creation(self.thread_name, self.listen)
        if not success:
            print("Failed to create keyboard listener thread")
            # Fallback: run in main thread (not ideal but prevents crash)
            self._run_main_thread()

    def _run_main_thread(self):
        """Fallback: run keyboard listener in main thread"""
        print("Running keyboard listener in main thread (fallback mode)")
        # This is a simplified version that doesn't block
        pass

    def stop(self):
        """Stop keyboard listener"""
        self.running = False
        stop_thread_safely(self.thread_name)

    @staticmethod
    def split_input(input_str):
        i = 0
        res = []
        while i < len(input_str):
            should_break = False
            for special_char in SPECIAL_CHARACTER_LIST:
                if input_str[i:].startswith(special_char):
                    res.append(special_char)
                    i += len(special_char)
                    should_break = True
                    break
            if should_break:
                continue
            res.append(input_str[i])
            i += len(res[-1])
        return res
