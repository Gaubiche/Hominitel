# Hominitel

This is a **work-in-progress MicroPython project** designed to run on **ESP32 boards**, specifically the ones developed by **Iodeo**, which are designed to be directly plugged into **Minitel terminals**.

The goal of this project is to **turn a Minitel into a Home Assistant control interface**.

---

## Current Features

- Connects to Home Assistant via its REST API.
- Displays a simple dashboard of Home Assistant entities (e.g., lights) and interacts with them.
- Development mode includes a built-in Minitel emulator via WebSockets.
- **Notification system**: Monitors a configurable entity and displays notifications with sound when its value changes.

## TODO
- [x] Add prompt mode
- [x] Add keymaps on screen
- [ ] Add a startup screen
- [ ] Add a way to make the configuration through the Minitel (wifi, api url, api token)
- [x] Add a way to customize the dashboard on the Minitel (e.g., add/remove entities, change layout, reorder, ...)
- [x] Create a notification system to display messages on the Minitel (with the minitel beep)
- [ ] Create a remote dev mode
- [ ] Add brightness control to lightbulbs
---

## Getting Started

### 1. Configuration

Create a `config.json` file at the root of the project with the following content:

```json
{
    "HA_API_URL": "<home-assistant-url>:8123/api",
    "HA_API_TOKEN": "Bearer <api_token>",
    "WIFI_SSID": "",
    "WIFI_PASSWORD": "",
    "DASHBOARD_TAB": {"entities":  ["<entity_id_1>", "<entity_id_2>"]},
    "NOTIFICATION_ENTITY": "input_text.notification"
}
```

#### Notification System

To enable the notification system, add the `NOTIFICATION_ENTITY` field to your configuration:

```json
{
    "HA_API_URL": "<home-assistant-url>:8123/api",
    "HA_API_TOKEN": "Bearer <api_token>",
    "WIFI_SSID": "",
    "WIFI_PASSWORD": "",
    "DASHBOARD_TAB": {
        "entities": [
            "light.living_room",
            "light.bedroom"
        ]
    },
    "NOTIFICATION_ENTITY": "input_text.notification"
}
```

When the value of the configured notification entity changes in Home Assistant, the Minitel will display a notification with a sound beep and show the new value.

**Note**: The notification entity is monitored independently from the dashboard entities, so you don't need to add it to the `DASHBOARD_TAB.entities` list.

### 2. Installation

1. Install [MicroPython](https://micropython.org/download/esp32/) on your ESP32 board.
2. Copy all Python files from the project root to the ESP32 using a tool like [mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html) or [ampy](https://github.com/scientifichackers/ampy).
3. Ensure the `config.json` file is also uploaded.

---

## 3. Development Mode

The emulator uses curses which does not natively run on Windows.

To simulate the Minitel environment on your local machine:

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Start the emulator server:
```bash
uvicorn hominitel.minitel.emulator_server:app --reload
```

3. Run the app
```bash
python -m hominitel
```

Now you can see the screen in the emulator server terminal and interact with it in the app terminal.
(Note: The emulator requires the enter key to be pressed to send an input, which is not the case on the Minitel)
