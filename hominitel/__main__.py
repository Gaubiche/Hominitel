import time

from hominitel.system import System

if __name__ == "__main__":
    system = System()
    system.run()
    try:
        while True:
            time.sleep(1)
    except Exception as e:
        system.stop()
        system.print("Shutdown")
