from conlib import *

class KEYS ():
    ArrowUp = "\x1b[A"
    ArrowDown = "\x1b[B"
    ArrowRight = "\x1b[C"
    ArrowLeft = "\x1b[D"
    BackSpace = "\x08"
    Delete = "\x7f"
    Enter = "\x0d"
    Tab = "\x09"
    Escape = "\x1b"

class Build ():

    def __init__ (self) -> None:
        self.user_pos : list[int, int] = [0, 0]
        self.box_pos : list[int, int] = [0, 0]
        self.screen_size : tuple[int, int] = get_size()

    def key_event (self, key : str) -> None:
        if key == KEYS.ArrowRight:
            print("arrow right")
        elif key == KEYS.ArrowLeft:
            print("arrow left")
        elif key == KEYS.ArrowUp:
            print("arrow up")
        elif key == KEYS.ArrowDown:
            print("arrow down")
        elif key == KEYS.Tab:
            print("tab")
        elif key in (KEYS.BackSpace, KEYS.Delete):
            print("backspace")
        elif key == KEYS.Enter:
            print("enter")
        elif key == KEYS.Escape:
            print("escape")
        else:
            print(key, hex(ord(key)))
    
    def run (self) -> None:
        while True:
            key = getchar(False)
            if key == "\x03":
                break
            self.key_event(key)

Build().run()