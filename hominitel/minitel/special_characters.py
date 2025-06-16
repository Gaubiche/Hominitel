class SpecialCharacters:
    ENTER = '\r'
    TAB = '\t'
    ARROW_UP = '\x1b[A'
    ARROW_DOWN = '\x1b[B'
    ARROW_RIGHT = '\x1b[C'
    ARROW_LEFT = '\x1b[D'
    ESCAPE = '\x1b'
    SEND = '\x13A'
    BACK = '\x13B'
    REPEAT = '\x13C'
    GUIDE = '\x13D'
    CANCEL = '\x13E'
    SUMMARY = '\x13F'
    CORRECT = '\x13G'

SPECIAL_CHARACTER_LIST = [getattr(SpecialCharacters, name) for name in dir(SpecialCharacters) if not name.startswith("__") and not callable(getattr(SpecialCharacters, name))]
SPECIAL_CHARACTER_NAMES = [name for name in dir(SpecialCharacters) if not name.startswith("__") and not callable(getattr(SpecialCharacters, name))]