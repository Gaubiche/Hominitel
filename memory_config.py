import gc

# Memory optimization settings
MEMORY_CONFIG = {
    "gc_threshold": 10000,  # Start GC when this many objects exist
    "gc_threshold_multiplier": 2,  # Multiply threshold after each GC
    
    # JSON parsing limits
    "max_json_size": 2048,  # Maximum JSON response size in bytes
    "max_string_length": 512,  # Maximum string length
    
    # HTTP request limits
    "max_response_size": 4096,  # Maximum HTTP response size
    "request_timeout": 10,  # Request timeout in seconds
    
    # Memory monitoring
    "memory_check_interval": 100,  # Check memory every N operations
    "emergency_cleanup_threshold": 0.15,  # Emergency cleanup when < 15% free
}

def configure_memory():
    """Configure memory settings for optimal performance"""
    try:
        # Set garbage collection thresholds
        gc.threshold(MEMORY_CONFIG["gc_threshold"])
        
        # Force initial cleanup
        gc.collect()
        
        print("Memory configuration applied")
        return True
        
    except Exception as e:
        print(f"Error configuring memory: {e}")
        return False

def get_memory_config():
    """Get current memory configuration"""
    return MEMORY_CONFIG.copy()

# Apply configuration on import
configure_memory()
