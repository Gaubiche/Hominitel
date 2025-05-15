import asyncio
import websockets
import json
import threading

from hominitel.minitel.adapter import Adapter
from hominitel.minitel.special_characters import SpecialCharacters


class EmulatorAdapter(Adapter):
    uri = "ws://localhost:8000/ws"
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        self.websocket = None
        self.connected_event = threading.Event()
        self._if_result = None
        self.input_buffer = []
        self.buffer_lock = threading.Lock()
        self._if_event = asyncio.Event()
        display_thread = threading.Thread(target=self._start_loop, daemon=True)
        input_thread = threading.Thread(target=self.listen_input, daemon=True)
        display_thread.start()
        input_thread.start()
        self._wait_for_connection()

    def listen_input(self):
        while True:
            user_input = input()
            with self.buffer_lock:
                self.input_buffer.append(user_input)

    def _start_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._connect_and_listen())

    def _wait_for_connection(self, timeout=5):
        if not self.connected_event.wait(timeout):
            raise TimeoutError("WebSocket connection could not be established.")

    async def _connect_and_listen(self):
        try:
            async with websockets.connect(self.uri) as websocket:
                self.websocket = websocket
                self.connected_event.set()
                while True:
                    data = await websocket.recv()
                    msg = json.loads(data)
                    if msg.get("type") == "if_result":
                        self._if_result = msg.get("value")
                        self._if_event.set()
        except Exception as e:
            print(f"WebSocket connection error: {e}")

    async def _send(self, mapping: dict):
        if self.websocket is None:
            raise ConnectionError("WebSocket is not connected.")
        await self.websocket.send(json.dumps(mapping))

    def send_command(self, mapping: dict):
        asyncio.run_coroutine_threadsafe(self._send(mapping), self.loop)

    def print(self, text: str):
        self.send_command({"type": "print", "text": text})

    def pos(self, row: int, col: int):
        self.send_command({"type": "pos", "row": row, "col": col-1})

    def cls(self):
        self.send_command({"type": "cls"})

    def inverse(self):
        self.send_command({"type": "inverse"})

    def echo_off(self):
        pass

    def get_input(self):
        with self.buffer_lock:
            if self.input_buffer:
                val = self.input_buffer.pop(0)
                if val == "":
                    return SpecialCharacters.ENTER
                return val.replace("\n", "")
        return None

