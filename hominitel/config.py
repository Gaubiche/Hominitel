import json

class Config:
    FIELDS = [
        "INITIALIZED", # has the initial configuration been done
        "HA_API_URL", # Home Assistant URL
        "HA_API_TOKEN", # Home Assistant API token
        "WIFI_SSID",
        "WIFI_PASSWORD",
        # tab configurations
        "DASHBOARD_TAB",
    ]

    def __init__(self):
        for field in self.FIELDS:
            setattr(self, field, None)
        self.debug = False

    def load(self):
        try:
            with open("config.json", "r") as file:
                config_data = json.load(file)
                for field in self.FIELDS:
                    setattr(self, field, config_data.get(field.upper(), getattr(self, field)))
        except FileNotFoundError:
            print("Configuration file not found.")
        except json.JSONDecodeError:
            print("Error decoding JSON configuration file.")

    def save(self):
        config_data = {field: getattr(self, field) for field in self.FIELDS}
        with open("config.json", "w") as file:
            json.dump(config_data, file, indent=4)

config = Config() # global config variable
config.load()