# Instantiation of the right adapter depending on the platform
try:
    from machine import UART # only accessible on ESP32
    from hominitel.minitel.pynitel_adapter import PynitelAdapter
    ON_MINITEL = True
except:
    from hominitel.minitel.emulator_adapter import SimuAdapter
    import curses
    ON_MINITEL = False

if ON_MINITEL:
    minitel = PynitelAdapter(UART(2, baudrate=1200, parity=0, bits=7, stop=1))
else:
    minitel = SimuAdapter()