import network
import time
import config

class WiFiConnection:
    def __init__(self):
        self.ssid = config.WIFI_SSID
        self.password = config.WIFI_PASSWORD
        self.wlan = network.WLAN(network.STA_IF)

    def connect(self):
        self.wlan.active(True)
        if not self.wlan.isconnected():
            print("Connecting to network...")
            self.wlan.connect(self.ssid, self.password)

            for _ in range(10):
                if self.wlan.isconnected():
                    break
                print(".", end="")
                time.sleep(1)

        if not self.wlan.isconnected():
            print("Failed to connect to the network.")
            time.sleep(10)
            raise Exception()