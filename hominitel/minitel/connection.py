import time
from hominitel import config

try:
    import network
    NETWORK_AVAILABLE = True
except ImportError:
    NETWORK_AVAILABLE = False

class WiFiConnection:
    def __init__(self):
        if NETWORK_AVAILABLE:
            self.ssid = config.WIFI_SSID
            self.password = config.WIFI_PASSWORD
            self.wlan = network.WLAN(network.STA_IF)

    def connect(self):
        if not NETWORK_AVAILABLE:
            return

        self.wlan.active(True)
        if not self.wlan.isconnected():
            self.wlan.connect(self.ssid, self.password)

            for _ in range(10):
                if self.wlan.isconnected():
                    break
                print(".", end="")
                time.sleep(1)

        if not self.wlan.isconnected():
            print("Failed to connect to the network.")
            raise Exception("WiFi connection failed")
