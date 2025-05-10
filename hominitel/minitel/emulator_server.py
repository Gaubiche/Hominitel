from fastapi import FastAPI, WebSocket
import json
import curses
import time

app = FastAPI()

class MinitelSimu:
    def __init__(self, stdscr, rows=25, cols=40):
        self.stdscr = stdscr
        self.rows = rows
        self.cols = cols
        self.win = curses.newwin(rows, cols, 0, 0)
        curses.noecho()
        curses.cbreak()
        self.inverse_mode = False

    def inverse(self):
        self.inverse_mode = True
        self.win.attron(curses.A_REVERSE)

    def inverse_off(self):
        self.inverse_mode = False
        self.win.attroff(curses.A_REVERSE)

    def echo_off(self):
        self.win.noecho()

    def pos(self, row: int, col: int):
        self.row = row
        self.col = col
        self.win.move(self.row, self.col)
        self.inverse_off()
        self.win.refresh()

    def _print(self, text: str):
        for ch in text:
            if self.col >= self.cols:
                self.row += 1
                self.col = 0
            if self.row >= self.rows:
                break
            self.win.addch(self.row, self.col, ch)
            self.win.refresh()
            time.sleep(0.02)
            self.col += 1
        self.win.refresh()

    def cls(self):
        self.win.clear()
        self.inverse_off()
        self.win.refresh()
        self.row, self.col = 0, 0


minitel =  curses.wrapper(MinitelSimu)
minitel.cls()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            cmd = json.loads(data)

            if cmd["type"] == "print":
                minitel._print(cmd["text"])

            elif cmd["type"] == "pos":
                minitel.pos(cmd["row"], cmd["col"])

            elif cmd["type"] == "cls":
                minitel.cls()

            elif cmd["type"] == "inverse":
                minitel.inverse()

        except Exception as e:
            print(f"WebSocket error: {e}")
            break
