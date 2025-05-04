# Hominitel

This is a **work-in-progress MicroPython project** designed to run on **ESP32 boards**, specifically the ones developed by **Iodeo**, which are designed to be directly plugged into **Minitel terminals**.

The goal of this project is to **turn a Minitel into a Home Assistant control interface**.

---

## Features/Goal

- Connects to Home Assistant via its REST API.
- Displays a simple dashboard of Home Assistant entities (e.g., lights) and interacts with them.
- Run prompts using Home Assistant assist API.
- Designed to run on ESP32 boards with MicroPython.
- Development mode includes a built-in Minitel emulator via WebSockets.

---

## Getting Started

### 1. Configuration

Create a `config.py` file at the root of the project with the following content:

```python
API_URL = "<home-assistant-url>:8123/api"
API_TOKEN = "Bearer <api_token>"
WIFI_SSID = ""  # Not needed for dev setup
WIFI_PASSWORD = ""  # Not needed for dev setup
ENTITIES = []  # List of Home Assistant entities to expose in the dashboard
```

### 2. Installation

1. Install [MicroPython](https://micropython.org/download/esp32/) on your ESP32 board.
2. Copy all Python files from the project root to the ESP32 using a tool like [mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html) or [ampy](https://github.com/scientifichackers/ampy).
3. Ensure the `config.py` file is also uploaded.

---

## 3. Development Mode

The emulator uses curses which does not natively run on Windows.

To simulate the Minitel environment on your local machine:

1. Make sure you have Python 3.9+ and [Uvicorn](https://www.uvicorn.org/) installed.
2. Start the emulator server:

```bash
cd api
uvicorn display_server:app --reload
```
3. Run main.py

