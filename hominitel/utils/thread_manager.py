import _thread
import time
import gc
from hominitel.utils.memory_manager import memory_manager

class ThreadManager:
    def __init__(self):
        self.threads = {}
        self.thread_count = 0
        self.max_threads = 6
        self.thread_lock = _thread.allocate_lock()
        
    def create_thread(self, name, target, args=(), daemon=True):
        with self.thread_lock:
            if name in self.threads and self.threads[name]['running']:
                print(f"Thread {name} already running, skipping creation")
                return False
                
            if self.thread_count >= self.max_threads:
                print(f"Thread limit reached ({self.max_threads}), cleaning up old threads")
                self._cleanup_old_threads()
                
            if self.thread_count >= self.max_threads:
                print(f"Cannot create thread {name}: limit exceeded")
                return False
            
            try:
                memory_manager.force_cleanup()

                thread_id = _thread.start_new_thread(target, args)
                
                self.threads[name] = {
                    'id': thread_id,
                    'target': target,
                    'args': args,
                    'running': True,
                    'created_at': time.time()
                }
                
                self.thread_count += 1
                print(f"Thread {name} created (ID: {thread_id}, Total: {self.thread_count})")
                return True
                
            except OSError as e:
                print(f"Failed to create thread {name}: {e}")
                self._cleanup_old_threads()
                memory_manager.force_cleanup()
                
                try:
                    thread_id = _thread.start_new_thread(target, args)
                    self.threads[name] = {
                        'id': thread_id,
                        'target': target,
                        'args': args,
                        'running': True,
                        'created_at': time.time()
                    }
                    self.thread_count += 1
                    print(f"Thread {name} created on retry (ID: {thread_id})")
                    return True
                except OSError as e2:
                    print(f"Failed to create thread {name} on retry: {e2}")
                    return False
            except Exception as e:
                print(f"Unexpected error creating thread {name}: {e}")
                return False
    
    def stop_thread(self, name):
        """Stop a thread by name"""
        with self.thread_lock:
            if name in self.threads and self.threads[name]['running']:
                self.threads[name]['running'] = False
                print(f"Thread {name} marked for stopping")
                return True
            return False
    
    def remove_thread(self, name):
        """Remove a thread from tracking"""
        with self.thread_lock:
            if name in self.threads:
                del self.threads[name]
                self.thread_count = max(0, self.thread_count - 1)
                print(f"Thread {name} removed from tracking")
                return True
            return False
    
    def _cleanup_old_threads(self):
        """Clean up old or stopped threads"""
        current_time = time.time()
        threads_to_remove = []
        
        for name, thread_info in self.threads.items():
            if current_time - thread_info['created_at'] > 120:
                threads_to_remove.append(name)
            elif not thread_info['running']:
                threads_to_remove.append(name)
        
        for name in threads_to_remove:
            self.remove_thread(name)
        
        if threads_to_remove:
            print(f"Cleaned up {len(threads_to_remove)} old threads")
    
    def cleanup_finished_threads(self):
        threads_to_remove = []
        
        for name, thread_info in self.threads.items():
            if not thread_info['running']:
                threads_to_remove.append(name)
        
        for name in threads_to_remove:
            self.remove_thread(name)
        
        if threads_to_remove:
            print(f"Cleaned up {len(threads_to_remove)} finished threads")
    
    def get_thread_info(self):
        with self.thread_lock:
            return {
                'count': self.thread_count,
                'max_threads': self.max_threads,
                'threads': {name: {
                    'running': info['running'],
                    'created_at': info['created_at']
                } for name, info in self.threads.items()}
            }
    
    def cleanup_all(self):
        with self.thread_lock:
            for name in list(self.threads.keys()):
                self.stop_thread(name)
                self.remove_thread(name)

thread_manager = ThreadManager()

def safe_thread_creation(name, target, args=(), daemon=True):
    """Safely create a thread with error handling"""
    return thread_manager.create_thread(name, target, args, daemon)

def stop_thread_safely(name):
    """Safely stop a thread"""
    return thread_manager.stop_thread(name)

def get_thread_status():
    """Get current thread status"""
    return thread_manager.get_thread_info()
