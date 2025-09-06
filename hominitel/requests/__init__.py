"""
Optimized requests module for ESP32/MicroPython
Memory-efficient HTTP client implementation
"""

import gc
import json
from hominitel.config import config

# Import memory configuration
try:
    from memory_config import MEMORY_CONFIG
except ImportError:
    # Fallback configuration if memory_config not available
    MEMORY_CONFIG = {
        "max_json_size": 2048,
        "max_response_size": 4096,
        "request_timeout": 10
    }

try:
    import urequests
    UREQUESTS_AVAILABLE = True
except ImportError:
    UREQUESTS_AVAILABLE = False

class MemoryEfficientResponse:
    """Memory-efficient response wrapper"""
    
    def __init__(self, response):
        self._response = response
        self._content = None
        self._json_data = None
        
    def close(self):
        """Close the response and free memory"""
        if hasattr(self._response, 'close'):
            self._response.close()
        self._content = None
        self._json_data = None
        gc.collect()
        
    @property
    def content(self):
        """Get response content with memory management"""
        if self._content is None:
            self._content = self._response.content
        return self._content
        
    def json(self):
        """Parse JSON with memory optimization"""
        if self._json_data is None:
            try:
                # Force garbage collection before parsing
                gc.collect()
                
                # Parse JSON with size limit
                content = self.content
                if len(content) > MEMORY_CONFIG["max_json_size"]:
                    raise MemoryError("JSON response too large")
                    
                self._json_data = json.loads(content)
                
                # Clear content to free memory
                self._content = None
                gc.collect()
                
            except MemoryError as e:
                print(f"Memory error parsing JSON: {e}")
                # Return minimal response
                self._json_data = {"error": "Memory allocation failed"}
            except Exception as e:
                print(f"JSON parsing error: {e}")
                self._json_data = {"error": "Invalid JSON response"}
                
        return self._json_data

def get(url, headers=None, timeout=10):
    """Memory-efficient GET request"""
    if not UREQUESTS_AVAILABLE:
        raise ImportError("urequests not available")
    
    try:
        # Force garbage collection before request
        gc.collect()
        
        response = urequests.get(url, headers=headers, timeout=MEMORY_CONFIG["request_timeout"])
        return MemoryEfficientResponse(response)
        
    except MemoryError as e:
        print(f"Memory error in GET request: {e}")
        gc.collect()
        raise
    except Exception as e:
        print(f"GET request error: {e}")
        gc.collect()
        raise

def post(url, headers=None, json_data=None, timeout=10):
    """Memory-efficient POST request"""
    if not UREQUESTS_AVAILABLE:
        raise ImportError("urequests not available")
    
    try:
        # Force garbage collection before request
        gc.collect()
        
        # Convert json to string if provided
        data = None
        if json_data is not None:
            data = json.dumps(json_data)
            
        response = urequests.post(url, headers=headers, data=data, timeout=MEMORY_CONFIG["request_timeout"])
        return MemoryEfficientResponse(response)
        
    except MemoryError as e:
        print(f"Memory error in POST request: {e}")
        gc.collect()
        raise
    except Exception as e:
        print(f"POST request error: {e}")
        gc.collect()
        raise
