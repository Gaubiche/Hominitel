import gc
import sys

class MemoryManager:
    def __init__(self):
        self.memory_warnings = 0
        self.max_memory_warnings = 5
        
    def get_memory_info(self):
        """Get current memory information"""
        try:
            # Get memory info if available
            if hasattr(gc, 'mem_free'):
                free_memory = gc.mem_free()
                allocated_memory = gc.mem_alloc()
                return {
                    "free": free_memory,
                    "allocated": allocated_memory,
                    "total": free_memory + allocated_memory
                }
            else:
                return {"free": "unknown", "allocated": "unknown", "total": "unknown"}
        except Exception as e:
            print(f"Error getting memory info: {e}")
            return {"free": "error", "allocated": "error", "total": "error"}
    
    def force_cleanup(self):
        """Aggressive memory cleanup"""
        try:
            # Run garbage collection multiple times
            for _ in range(3):
                gc.collect()
            
            # Clear any cached objects if possible
            if hasattr(gc, 'threshold'):
                gc.threshold(gc.threshold())
                
            return True
        except Exception as e:
            print(f"Error during memory cleanup: {e}")
            return False
    
    def check_memory_pressure(self):
        """Check if system is under memory pressure"""
        try:
            memory_info = self.get_memory_info()
            
            if memory_info["free"] != "unknown" and memory_info["total"] != "unknown":
                free_ratio = memory_info["free"] / memory_info["total"]
                
                # If less than 20% memory free, consider it pressure
                if free_ratio < 0.2:
                    self.memory_warnings += 1
                    print(f"Memory pressure detected: {free_ratio:.1%} free")
                    
                    if self.memory_warnings >= self.max_memory_warnings:
                        print("Too many memory warnings, forcing cleanup")
                        self.force_cleanup()
                        self.memory_warnings = 0
                    
                    return True
            
            return False
            
        except Exception as e:
            print(f"Error checking memory pressure: {e}")
            return False
    
    def safe_execute(self, func, *args, **kwargs):
        """Safely execute a function with memory management"""
        try:
            # Check memory before execution
            if self.check_memory_pressure():
                self.force_cleanup()
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Cleanup after execution
            gc.collect()
            
            return result
            
        except MemoryError as e:
            print(f"Memory error in safe_execute: {e}")
            self.force_cleanup()
            raise
        except Exception as e:
            print(f"Error in safe_execute: {e}")
            gc.collect()
            raise
    
    def monitor_memory(self):
        """Monitor memory usage and log warnings"""
        memory_info = self.get_memory_info()
        print(f"Memory: Free={memory_info['free']}, Allocated={memory_info['allocated']}")

# Global memory manager instance
memory_manager = MemoryManager()

def safe_memory_operation(func):
    """Decorator for memory-safe operations"""
    def wrapper(*args, **kwargs):
        return memory_manager.safe_execute(func, *args, **kwargs)
    return wrapper

def emergency_cleanup():
    """Emergency memory cleanup for critical situations"""
    try:
        # Force multiple garbage collections
        for _ in range(5):
            gc.collect()
        
        # Clear any possible caches
        if hasattr(sys, 'intern'):
            # Clear string intern cache if possible
            pass
            
        print("Emergency cleanup completed")
        return True
        
    except Exception as e:
        print(f"Emergency cleanup failed: {e}")
        return False
